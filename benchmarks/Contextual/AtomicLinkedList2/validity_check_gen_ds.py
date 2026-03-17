from z3 import *

# --- Define variables from CHC ---
N = Int('N')
k = Int('k')
k1 = Int('k1')
len = Int('len')
len1 = Int('len1')
items_processed = Int('items_processed')
items_processed1 = Int('items_processed1')
ret = Int('ret')
ret1 = Int('ret1')
max = Int('max')
max1 = Int('max1')

# --- Define constants from CHC ---
MAX = 128
MIN = -129

# Global flag to track if all checks pass
chckval = 1

try:
    from llm_definitions import inv1, inv2, insertHead, popHead, fail
    print("Successfully imported definitions from llm_definitions.py")
except ImportError:
    print("ERROR: Could not import from 'llm_definitions.py'.")
    print("Please ensure the file exists and defines: inv1, inv2, insertHead, popHead, fail")
    exit()
except Exception as e:
    print(f"An error occurred during import: {e}")
    exit()

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
        try:
            print("Model:", s.model())
        except Exception as e:
            print(f"Could not print model due to error: {e}")
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
    """Checks: (rule (=> (and (> N 0) (= k1 0) (= len1 0)) (inv1 k1 N len1)))"""
    antecedent = And(N > 0, k1 == 0, len1 == 0, min == MAX, max == MIN)
    consequent = inv1(k1, N, min, max, len1)
    check_implication(antecedent, consequent, "Initial inv1")

def chk_rule_2_loop1_insert():
    """Checks: (rule (=> (and (inv1 k N len) (< k N) (insertHead k len len1) (= k1 (+ k 1))) (inv1 k1 N len1)))"""
    antecedent = And(
        inv1(k, N,min, max, len),
        k < N,
        insertHead(k, min, max, len, min1, max1, len1),
        k1 == (k + 1)
    )
    consequent = inv1(k1, N, min1, max1, len1)
    check_implication(antecedent, consequent, "Loop 1 Inductiveness (insertHead)")

def chk_rule_3_transition_inv2():
    """Checks: (rule (=> (and (inv1 k N len) (not (< k N)) (= items_processed 0) (= ret1 MAX) (= max1 MIN)) (inv2 len items_processed max1 ret1)))"""
    antecedent = And(
        inv1(k, N, min, max, len),
        Not(k < N),
        items_processed == 0,
        ret1 == MAX
    )
    consequent = inv2(min, max, len, items_processed, ret1)
    check_implication(antecedent, consequent, "Transition inv1 -> inv2")

def chk_rule_4_loop2_pop():
    """Checks: (rule (=> (and (inv2 len items_processed max ret) (not (= len 0)) (popHead len len1 max1 ret1) (= items_processed1 (+ items_processed 1))) (inv2 len1 items_processed1 max1 ret1)))"""
    antecedent = And(
        inv2(min, max, len, items_processed, ret),
        Not(len == 0),
        popHead(min, max, len, min1, max1, len1, ret1),
        items_processed1 == (items_processed + 1)
    )
    consequent = inv2(min1, max1, len1, items_processed1, ret1)
    check_implication(antecedent, consequent, "Loop 2 Inductiveness (popHead)")

def chk_rule_5_post_fail():
    """Checks: (rule (=> (and (inv2 len items_processed max ret) (= len 0) (not (= ret 0))) fail))"""
    global chckval
    print("\n" + "="*52)
    print("Checking Rule: Post-Condition (Fail)")
    print("="*52)
    
    # This is the condition that leads to failure
    correct_condition = (ret == 0)
    
    antecedent = And(
        inv2(min, max, len, items_processed, ret),
        len == 0,
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
chk_rule_2_loop1_insert()
chk_rule_3_transition_inv2()
chk_rule_4_loop2_pop()
chk_rule_5_post_fail()

# --- Final check to print the success string ---
if chckval == 1:
    print("\n" + "="*52)
    print("All implications are valid and the fail state is unreachable.")
    print("qwertyasdfg")
else:
    print("\n" + "="*52)
    print("One or more checks failed. See log above for details.")