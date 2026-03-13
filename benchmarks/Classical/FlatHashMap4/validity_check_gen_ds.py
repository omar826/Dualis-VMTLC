from z3 import *

# --- Define variables from CHC ---
N = Int('N')
i = Int('i')
i1 = Int('i1')
containsk = Int('containsk')
containsk1 = Int('containsk1')
len = Int('len')
len1 = Int('len1')
flag = Int('flag')
flag1 = Int('flag1')
ret = Int('ret')
ret1 = Int('ret1')
k = Int('k')
v = Int('v')

# --- Define constants from CHC ---
MAX = 128

# Global flag to track if all checks pass
chckval = 1

try:
    from llm_definitions import inv1, inv2, insert, erase
    print("Successfully imported definitions from llm_definitions.py")
except ImportError:
    print("ERROR: Could not import from 'llm_definitions.py'.")
    print("Please ensure the file exists and defines: inv1, inv2, insert, erase")
    exit()
except Exception as e:
    print(f"An error occurred during import: {e}")
    exit()

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
        # print("Model:", s.model()) # Disabling model print to avoid Unicode errors
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
        try:
            print("Model:", s.model())
        except Exception as e:
            print(f"Could not print model due to error: {e}")
        chckval = 0 # This is a definite failure
    else:
        print("✅ Implication is VALID")
    s.pop()

def chk_rule_1_init_inv1():
    """Checks: (rule (=> (and (> N 0) (= i 0) (= len 0)) (inv1 i N len)))"""
    antecedent = And(N > 0, i == 0, len == 0)
    consequent = inv1(i, N, len)
    check_implication(antecedent, consequent, "Initial inv1")

def chk_rule_2_loop1():
    """Checks: (rule (=> (and (inv1 i N len) (is_valid containsk1) (< i N) (= k i) (= v i) (insert k v len 0 len1 containsk1) (= i1 (+ i 1))) (inv1 i1 N len1)))"""
    antecedent = And(
        inv1(i, N, len),
        is_valid(containsk1),
        i < N,
        k == i,
        v == i,
        insert(k, v, len, 0, len1, containsk1),
        i1 == (i + 1)
    )
    consequent = inv1(i1, N, len1)
    check_implication(antecedent, consequent, "Loop 1 Inductiveness (insert)")

def chk_rule_3_transition_inv2():
    """Checks: (rule (=> (and (inv1 i N len) (is_valid flag) (not (< i N)) (= i1 0) (= flag 0) (= ret1 MAX)) (inv2 i1 N len flag ret1)))"""
    antecedent = And(
        inv1(i, N, len),
        is_valid(flag),
        Not(i < N),
        i1 == 0,
        flag == 0,
        ret1 == MAX
    )
    consequent = inv2(i1, N, len, flag, ret1)
    check_implication(antecedent, consequent, "Transition to inv2")

def chk_rule_4_loop2_erase():
    """Checks: (rule (=> (and (inv2 i N len flag ret) (< i N) (is_valid flag) (= flag 1) (= k i) (erase k len flag len1 ret1) (= i1 (+ i 1)) (= flag1 (- 1 flag))) (inv2 i1 N len1 flag1 ret1)))"""
    antecedent = And(
        inv2(i, N, len, flag, ret),
        i < N,
        is_valid(flag),
        flag == 1,
        k == i,
        erase(k, len, flag, len1, ret1),
        i1 == (i + 1),
        flag1 == (1 - flag)
    )
    consequent = inv2(i1, N, len1, flag1, ret1)
    check_implication(antecedent, consequent, "Loop 2 Inductiveness (Erase Branch)")

def chk_rule_5_loop2_skip():
    """Checks: (rule (=> (and (inv2 i N len flag ret) (< i N) (is_valid flag) (= flag 0) (= i1 (+ i 1)) (= flag1 (- 1 flag))) (inv2 i1 N len flag1 ret)))"""
    antecedent = And(
        inv2(i, N, len, flag, ret),
        i < N,
        is_valid(flag),
        flag == 0,
        i1 == (i + 1),
        flag1 == (1 - flag)
    )
    consequent = inv2(i1, N, len, flag1, ret)
    check_implication(antecedent, consequent, "Loop 2 Inductiveness (Skip Branch)")

def chk_rule_6_post_fail():
    """Checks: (rule (=> (and (inv2 i N len flag ret) (is_valid flag) (not (< i N)) (not (=> (= flag 0) (= ret (- N 1))))) fail))"""
    global chckval
    print("\n" + "="*52)
    print("Checking Rule: Post-Condition (Fail)")
    print("="*52)
    
    # This is the condition that leads to failure
    correct_condition = Implies(flag == 0, ret == (N - 1))
    
    antecedent = And(
        inv2(i, N, len, flag, ret),
        is_valid(flag),
        Not(i < N),
        Not(correct_condition)
    )
    
    consequent = fail()
    ic_implication = Implies(antecedent, consequent)

    # We check if this failure-inducing condition is *ever* satisfiable
    s.push()
    print("Antecedent (Fail Condition):", antecedent)
    s.add(antecedent)
    print("Checking if fail condition is satisfiable...")
    if s.check() == sat:
        print("❌ FAILURE: The fail condition is satisfiable (property is VIOLATED):")
        try:
            print("Model:", s.model())
        except Exception as e:
            print(f"Could not print model due to error: {e}")
        chckval = 0
    else:
        print("✅ SUCCESS: The fail condition is NOT satisfiable (property holds).")
    s.pop()


# --- Run all checks ---
chk_rule_1_init_inv1()
chk_rule_2_loop1()
chk_rule_3_transition_inv2()
chk_rule_4_loop2_erase()
chk_rule_5_loop2_skip()
chk_rule_6_post_fail()

# --- Final check to print the success string ---
if chckval == 1:
    print("\n" + "="*52)
    print("All implications are valid and the fail state is unreachable.")
    print("qwertyasdfg")
else:
    print("\n" + "="*52)
    print("One or more checks failed. See log above for details.")