from z3 import *

# --- Define variables from the new CHC ---
N = Int('N')
len = Int('len')
len1 = Int('len1')
i = Int('i')
i1 = Int('i1')
i_old = Int('i_old')
min = Int('min')
min1 = Int('min1')
max = Int('max')
max1 = Int('max1')
kveq = Int('kveq')
kveq1 = Int('kveq1')
k = Int('k')
v = Int('v')
ret1 = Int('ret1')
# Note: is_valid is a function, not a variable
# Note: size, containsmru, etc. are not in this CHC

# --- Define constants from CHC ---
MAX = 128
MIN = -129

# Global flag to track validity
chckval = 1

# --- Import LLM-generated functions ---
try:
    # Import the relations defined in the new CHC
    from llm_definitions import inv1, inv2, insert, find, insert1
    print("Successfully imported definitions from llm_definitions.py")
except ImportError:
    print("ERROR: Could not import from 'llm_definitions.py'.")
    print("Please ensure the file exists and defines: inv1, inv2, insert, find")
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

    # Check if the implication is valid (i.e., if Not(implication) is unsatisfiable)
    s.push()
    print("\nImplication:", implication)
    s.add(Not(implication))
    print("Checking validity of implication (searching for counterexample)...")
    if s.check() == sat:
        print("❌ COUNTEREXAMPLE FOUND (Implication is NOT valid):")
        print("Model:", s.model())
        chckval = 0 # This is a definite failure

    else:
        print("✅ Implication is VALID")
    s.pop()

def chk_rule_1_init():
    """Checks: (rule (=> (and (> N 0) (= len 0) (= i 0) (= min MAX) (= max MIN) (= kveq 1)) (inv1 i N len min max kveq)))"""
    antecedent = And(N > 0, len == 0, i == 0, min == MAX, max == MIN, kveq == 1)
    consequent = inv1(i, N, len, min, max, kveq)
    check_implication(antecedent, consequent, "Initial Conditions")

def chk_rule_2_loop1():
    """Checks: (rule (=> (and (inv1 i N len min max kveq) (is_valid kveq) (< i N) (= k i) (= v i) (insert k v len min max kveq len1 min1 max1 kveq1) (= i1 (+ i 1))) (inv1 i1 N len1 min1 max1 kveq1)))"""
    antecedent = And(
        inv1(i, N, len, min, max, kveq),
        is_valid(kveq),
        i < N,
        k == i,
        v == i,
        insert(k, v, len, min, max, kveq, len1, min1, max1, kveq1), # 10 args
        i1 == (i + 1)
    )
    consequent = inv1(i1, N, len1, min1, max1, kveq1)
    check_implication(antecedent, consequent, "Loop 1 Inductiveness")

def chk_rule_3_transition():
    """Checks: (rule (=> (and (inv1 i_old N len min max kveq) (is_valid kveq) (not (< i_old N)) (= i 0)) (inv2 i N len min max kveq)))"""
    antecedent = And(
        inv1(i_old, N, len, min, max, kveq),
        is_valid(kveq),
        Not(i_old < N),
        i == 0
    )
    consequent = inv2(i, N, len, min, max, kveq)
    check_implication(antecedent, consequent, "Transition to Loop 2")

def chk_rule_4_loop2():
    """Checks: (rule (=> (and (inv2 i N len min max kveq) (is_valid kveq) (< i N) (= k i) (= v i) (insert k v len min max kveq len1 min1 max1 kveq1) (= i1 (+ i 1))) (inv2 i1 N len1 min1 max1 kveq1)))"""
    antecedent = And(
        inv2(i, N, len, min, max, kveq),
        is_valid(kveq),
        i < N,
        k == i,
        v == i,
        insert1(k, v, len, min, max, kveq, len1, min1, max1, kveq1), # 10 args
        i1 == (i + 1)
    )
    consequent = inv2(i1, N, len1, min1, max1, kveq1)
    check_implication(antecedent, consequent, "Loop 2 Inductiveness")

def chk_rule_5_fail():
    """Checks: (rule (=> (and (inv2 i N len min max kveq) (is_valid kveq) (not (< i N)) (and (>= k 0) (< k N ) (= k min)) (find k len min max kveq ret1) (= ret1 MAX)) fail))"""
    global chckval
    print("\n" + "="*52)
    print("Checking Rule: Post-Condition (Fail)")
    print("="*52)
    
    # This is the condition that leads to failure
    antecedent = And(
        inv2(i, N, len, min, max, kveq),
        is_valid(kveq),
        Not(i < N),
        And(k >= 0, k < N, k == min),
        find(k, len, min, max, kveq, ret1), # 6 args
        ret1 == MAX
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
chk_rule_2_loop1()
chk_rule_3_transition()
chk_rule_4_loop2()
chk_rule_5_fail()

# --- Final check to print the success string ---
if chckval == 1:
    print("\n" + "="*52)
    print("All implications are valid and the fail state is unreachable.")
    print("qwertyasdfg")
else:
    print("\n" + "="*52)
    print("One or more checks failed. See log above for details.")