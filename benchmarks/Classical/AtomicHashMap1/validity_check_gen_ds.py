from z3 import *

# Define variables from CHC
N = Int('N')
i = Int('i')
i1 = Int('i1')
k = Int('k')
k1 = Int('k1')
len_var = Int('len')
len1 = Int('len1')
len2 = Int('len2')
min_var = Int('min')
min1 = Int('min1')
min2 = Int('min2')
max_var = Int('max')
max1 = Int('max1')
max2 = Int('max2')
kveq = Int('kveq')
kveq1 = Int('kveq1')
kveq2 = Int('kveq2')
v = Int('v')
v1 = Int('v1')
ret1 = Int('ret1')

# Define constants from CHC
MAX = 128
MIN = -129

# Global flag to track if all checks pass
chckval = 1

try:
    from llm_definitions import inv1, insert, find
    print("Successfully imported definitions from llm_definitions.py")
except ImportError:
    print("ERROR: Could not import from 'llm_definitions.py'.")
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

def chk_val_initial_conditions():
    global chckval
    print("="*53)
    print("Checking if initial conditions imply loop invariant")
    print("="*53)
    
    # CHC Rule: (=> (and (> N 0) (= len 0) (= i 0) (= min MAX) (= max MIN) (= kveq 1) ) (inv1...))
    ic_antecedent = And(N > 0,
                        len_var == 0,
                        i == 0,
                        min_var == MAX,
                        max_var == MIN)
    ic_consequent = inv1(i, N, len_var, min_var, max_var)
    ic_implication = Implies(ic_antecedent, ic_consequent)

    s.push()
    print("\nImplication:", ic_implication)
    s.add(Not(ic_implication))
    print("Checking validity of implication:")
    if s.check() == sat:
        print("Counterexample found (Implication is not valid):")
        print("Model:", s.model())
        chckval = 0
    else:
        print("Implication is valid")
    s.pop()

def chk_val_invariant():
    global chckval
    print("="*40)
    print("Checking for loop inductiveness")
    print("="*40)
    
    # CHC Rule: (=> (and (inv1...) (is_valid kveq) (< i N) (= k i) (= v i) (insert...) (is_valid kveq1) (= v1 (+ i 1)) (insert...) (= i1 (+ i 1))) (inv1...))
    ic_antecedent = And(inv1(i, N, len_var, min_var, max_var),
                        i < N,
                        k == i,
                        v == i,
                        insert(k, v, len_var, min_var, max_var, len1, min1, max1),
                        is_valid(kveq1),
                        v1 == (i + 1),
                        insert(k, v1, len1, min1, max1, len2, min2, max2),
                        i1 == (i + 1))
    ic_consequent = inv1(i1, N, len2, min2, max2)
    ic_implication = Implies(ic_antecedent, ic_consequent)

    s.push()
    print("\nImplication:", ic_implication)
    s.add(Not(ic_implication))
    print("Checking validity of implication:")
    if s.check() == sat:
        print("Counterexample found (Implication is not valid):")
        print("Model:", s.model())
        chckval = 0
    else:
        print("Implication is valid")
    s.pop()

def chk_post():
    global chckval
    print("="*20)
    print("   Checking post   ")
    print("="*20)
    # CHC Rule: (=> (and (inv1...) (not (< i N)) (<= 0 k) (< k N) (find...) (not (= ret1 k))) fail))
    correct_condition = Not(ret1 == MIN)
    ic_antecedent = And(inv1(i, N, len_var, min_var, max_var),
                        Not(i < N),
                        k >= 0,
                        k < N,
                        find(k, len_var, min_var, max_var, ret1),
                        Not(correct_condition))

    ic_consequent = fail()
    ic_implication = Implies(ic_antecedent, ic_consequent)

    s.push()
    print("\nImplication:", ic_implication)
    s.add(Not(ic_implication))
    print("Checking validity of implication:")
    if s.check() == sat:
        print("Counterexample found (Implication is not valid):")
        print("Model:", s.model())
        chckval = 0
    else:
        # For the post-condition, validity means the property holds
        print("Implication is valid (Property holds)")
    s.pop()

# --- Run all checks ---
chk_val_initial_conditions()
chk_val_invariant()
chk_post()

# --- Final result ---
if chckval == 1:
    print("\nqwertyasdfg")