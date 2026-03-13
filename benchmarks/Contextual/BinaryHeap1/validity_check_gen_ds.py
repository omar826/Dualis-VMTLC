from z3 import *

# --- Define variables from CHC ---
N = Int('N')
i = Int('i')
i1 = Int('i1')
isHeap = Int('isHeap')
isHeap1 = Int('isHeap1')
isHeap2 = Int('isHeap2')
isHeap3 = Int('isHeap3')
min = Int('min')
min1 = Int('min1')
max = Int('max')
max1 = Int('max1')
len = Int('len')
len1 = Int('len1')
d = Int('d')
d1 = Int('d1')
ret = Int('ret')
ret1 = Int('ret1')

# --- Define constants from CHC ---
MAX = 128
MIN = -129

# Global flag to track if all checks pass
chckval = 1

try:
    from llm_definitions import inv1, inv2, insert, deleteMin, downHeap, fail
    print("Successfully imported definitions from llm_definitions.py")
except ImportError:
    print("ERROR: Could not import from 'llm_definitions.py'.")
    print("Please ensure the file exists and defines: inv1, inv2, insert, deleteMin, downHeap, fail")
    exit()
except Exception as e:
    print(f"An error occurred during import: {e}")
    exit()

def is_valid(x):
    """CHC Helper: (define-fun is_valid ((x Int)) Bool (or (= x 1) (= x 0)))"""
    return Or(x == 1, x == 0)

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
    """Checks: (rule (=> (and (> N 0) (= i1 0) (= isHeap1 1) (= len1 0) (= min MAX) (= max MIN)) (inv1 i1 N isHeap1 min max len1)))"""
    antecedent = And(
        N > 0,
        i1 == 0,
        isHeap1 == 1,
        len1 == 0,
        min == MAX,
        max == MIN
    )
    consequent = inv1(i1, N, isHeap1, min, max, len1)
    check_implication(antecedent, consequent, "Initial inv1")

def chk_rule_2_loop1_insert():
    """Checks: (rule (=> (and (inv1 i N isHeap min max len) (is_valid isHeap) (< i N) (insert i isHeap min max len isHeap1 min1 max1 len1) (= i1 (+ i 1))) (inv1 i1 N isHeap1 min1 max1 len1)))"""
    antecedent = And(
        inv1(i, N, isHeap, min, max, len),
        is_valid(isHeap),
        i < N,
        insert(i, isHeap, min, max, len, isHeap1, min1, max1, len1),
        i1 == (i + 1)
    )
    consequent = inv1(i1, N, isHeap1, min1, max1, len1)
    check_implication(antecedent, consequent, "Loop 1 Inductiveness (insert)")

def chk_rule_3_transition_inv2():
    """Checks: (rule (=> (and (inv1 i N isHeap min max len) (is_valid isHeap) (not (< i N)) (= d 0) (= ret MAX)) (inv2 d N min max len isHeap ret)))"""
    antecedent = And(
        inv1(i, N, isHeap, min, max, len),
        is_valid(isHeap),
        Not(i < N),
        d == 0,
        ret == MAX
    )
    consequent = inv2(d, N, min, max, len, isHeap, ret)
    check_implication(antecedent, consequent, "Transition inv1 -> inv2")

def chk_rule_4_loop2_delete():
    """Checks: (rule (=> (and (inv2 d N min max len isHeap ret) (is_valid isHeap) (is_valid isHeap2) (not (= len 0)) (deleteMin min max len isHeap min1 max1 len1 ret1 isHeap1) (downHeap isHeap2) (= d1 (+ d 1))) (inv2 d1 N min1 max1 len1 isHeap2 ret1)))"""
    antecedent = And(
        inv2(d, N, min, max, len, isHeap, ret),
        is_valid(isHeap),
        is_valid(isHeap2),
        Not(len == 0),
        deleteMin(min, max, len, isHeap, min1, max1, len1, ret1, isHeap1),
        downHeap(isHeap2),
        d1 == (d + 1)
    )
    consequent = inv2(d1, N, min1, max1, len1, isHeap2, ret1)
    check_implication(antecedent, consequent, "Loop 2 Inductiveness (deleteMin/downHeap)")

def chk_rule_5_post_fail():
    """Checks: (rule (=> (and (inv2 d N min max len isHeap ret) (is_valid isHeap) (= len 0) (not (and (= ret (- N 1)) (= isHeap 1)))) fail))"""
    global chckval
    print("\n" + "="*52)
    print("Checking Rule: Post-Condition (Fail)")
    print("="*52)
    
    # This is the condition that leads to failure
    correct_condition = And(ret == (N - 1), isHeap == 1)
    
    antecedent = And(
        inv2(d, N, min, max, len, isHeap, ret),
        is_valid(isHeap),
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
chk_rule_4_loop2_delete()
chk_rule_5_post_fail()

# --- Final check to print the success string ---
if chckval == 1:
    print("\n" + "="*52)
    print("All implications are valid and the fail state is unreachable.")
    print("qwertyasdfg")
else:
    print("\n" + "="*52)
    print("One or more checks failed. See log above for details.")