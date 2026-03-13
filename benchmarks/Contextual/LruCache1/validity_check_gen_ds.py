from z3 import *

# --- Define variables from the new CHC ---
N = Int('N')
size = Int('size')
len = Int('len')
len1 = Int('len1')
i = Int('i')
i1 = Int('i1')
containsmru = Int('containsmru')
containsmru1 = Int('containsmru1')
containsk = Int('containsk')
mru = Int('mru')
mru1 = Int('mru1')
k = Int('k')
v = Int('v')
ret1 = Int('ret1')
# Note: kveq and kveq1 are NOT in this CHC

# --- Define constants from CHC ---
MAX = Const('MAX', IntSort())

# Global flag to track validity
chckval = 1

# --- Import LLM-generated functions ---
try:
    # Import the relations defined in the new CHC
    from llm_definitions import inv1, insert_or_assign, find
    print("Successfully imported definitions from llm_definitions.py")
except ImportError:
    print("ERROR: Could not import from 'llm_definitions.py'.")
    print("Please ensure the file exists and defines: inv1, insert_or_assign, find")
    exit()
except Exception as e:
    print(f"An error occurred during import: {e}")
    exit()

# --- CHC Helper Functions ---
def is_valid(x):
    """CHC Helper: (define-fun is_valid ((x Int)) Bool (or (= x 1) (= x 0)))"""
    return Or(x == 1, x == 0)

def fail():
    """Represents the failure state."""
    return BoolVal(False)

# Create a single solver
s = Solver()

# Add the constant definitions to the solver
s.add(MAX == 128)

def check_implication(antecedent, consequent, rule_name):
    """
    Helper function to check a single Z3 implication.
    Returns True if valid, False otherwise.
    """
    global chckval
    print("\n" + "="*52)
    print(f"Checking Rule: {rule_name}")
    print("="*52)
    
    implication = Implies(antecedent, consequent)
    
    # Check if the antecedent (the "if" part) can even be true
    s.push()
    print("Antecedent:", antecedent)
    s.add(antecedent)
    print("Checking if antecedent is satisfiable...")
    if s.check() == sat:
        print("Antecedent is satisfiable")
        print("Model:", s.model())
    else:
        print("Antecedent is always false (rule is trivially valid)")
    s.pop()

    # Check if the implication is valid (i.e., if Not(implication) is unsatisfiable)
    s.push()
    print("\nImplication:", implication)
    s.add(Not(implication))
    print("Checking validity of implication (searching for counterexample)...")
    if s.check() == sat:
        print("❌ COUNTEREXAMPLE FOUND (Implication is NOT valid):")
        print("Model:", s.model())
        chckval = 0 # This is a definite failure
        s.pop()
        return False
    else:
        print("✅ Implication is VALID")
        s.pop()
        return True

def chk_rule_1_init():
    """Checks: (rule (=> (and (>= N 3) (= size N) (= len 0) (= i 0) (= containsmru 0) (= containsk 0) (= mru MAX)) (inv1 i N len mru size containsmru containsk)))"""
    antecedent = And(
        N >= 3,
        size == N,
        len == 0,
        i == 0,
        containsmru == 0,
        containsk == 0,
        mru == MAX
    )
    # inv1(i, N, len, mru, size, containsmru, containsk) - 7 args
    consequent = inv1(i, N, len, mru, size, containsmru, containsk)
    check_implication(antecedent, consequent, "Initial Conditions")

def chk_rule_2_loop_insert():
    """Checks: (rule (=> (and (inv1 i N len mru size containsmru containsk) (is_valid containsmru) (< i N) (= k i) (= v i) (insert_or_assign k v len mru size containsmru len1 mru1 containsmru1 ret1) (= i1 (+ i 1))) (inv1 i1 N len1 mru1 size containsmru1 containsk)))"""
    antecedent = And(
        # inv1(i, N, len, mru, size, containsmru, containsk) - 7 args
        inv1(i, N, len, mru, size, containsmru, containsk),
        is_valid(containsmru),
        i < N,
        k == i,
        v == i,
        # insert_or_assign(k, v, len, mru, size, containsmru, len1, mru1, containsmru1, ret1) - 10 args
        insert_or_assign(k, v, len, mru, size, containsmru, len1, mru1, containsmru1, ret1),
        i1 == (i + 1)
    )
    # inv1(i1, N, len1, mru1, size, containsmru1, containsk) - 7 args
    consequent = inv1(i1, N, len1, mru1, size, containsmru1, containsk)
    check_implication(antecedent, consequent, "Loop Inductiveness (Insert)")

def chk_rule_3_post_fail():
    """Checks: (rule (=> (and (inv1 i N len mru size containsmru containsk) (is_valid containsmru) (is_valid containsk) (not (< i N)) (<= 0 k) (< k N) (find k containsk mru1) (= mru1 MAX)) fail))"""
    global chckval
    print("\n" + "="*52)
    print("Checking Rule: Post-Condition (Fail)")
    print("="*52)
    
    # This is the condition that leads to failure
    antecedent = And(
        # inv1(i, N, len, mru, size, containsmru, containsk) - 7 args
        inv1(i, N, len, mru, size, containsmru, containsk),
        is_valid(containsmru),
        is_valid(containsk),
        Not(i < N),
        0 <= k,
        k < N,
        # find(k, containsk, mru1) - 3 args
        find(k, containsk, mru1),
        mru1 == MAX
    )
    
    # We check if this failure-inducing condition is *ever* satisfiable
    s.push()
    print("Antecedent (Fail Condition):", antecedent)
    s.add(antecedent)
    print("Checking if fail condition is satisfiable...")
    if s.check() == sat:
        print("❌ FAILURE: The fail condition is satisfiable (property is VIOLATED):")
        print("Model:", s.model())
        chckval = 0
    else:
        print("✅ SUCCESS: The fail condition is NOT satisfiable (property holds).")
    s.pop()


# --- Run all checks ---
chk_rule_1_init()
chk_rule_2_loop_insert()
chk_rule_3_post_fail()

# --- Final check to print the success string ---
if chckval == 1:
    print("\n" + "="*52)
    print("All implications are valid and the fail state is unreachable.")
    print("qwertyasdfg")
else:
    print("\n" + "="*52)
    print("One or more checks failed. See log above for details.")