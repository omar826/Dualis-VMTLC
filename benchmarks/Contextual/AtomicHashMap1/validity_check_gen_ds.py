from z3 import *

# Define variables from CHC
N = Int('N')
k = Int('k')
k1 = Int('k1')
len_var = Int('len')
len1 = Int('len1')
len_inter = Int('len_inter')
min_var = Int('min')
min1 = Int('min1')
min_inter = Int('min_inter')
max_var = Int('max')
max1 = Int('max1')
max_inter = Int('max_inter')
containsk = Int('containsk')
containsk1 = Int('containsk1')
containsk_inter = Int('containsk_inter')
v_first = Int('v_first')
v_second = Int('v_second')
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
    # CHC Rule: (=> (and (> N 0) (= k 0) (= len 0) (= min MAX) (= max MIN) (= containsk 0)) (inv1 k N len min max containsk))
    ic_antecedent = And(N > 0, k == 0, len_var == 0, min_var == MAX, max_var == MIN, containsk == 0)
    ic_consequent = inv1(k, N, len_var, min_var, max_var, containsk)
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
    # CHC Rule: (=> (and (inv1...) (< k N) (insert...) (insert1...) (= k1 (+ k 1))) (inv1...))
    ic_antecedent = And(inv1(k, N, len_var, min_var, max_var, containsk),
                        is_valid(containsk),
                        k < N,
                        v_first == k,
                        insert(k, v_first, len_var, min_var, max_var, containsk, len_inter, min_inter, max_inter, containsk_inter),
                        v_second == k + 1,
                        insert(k, v_second, len_inter, min_inter, max_inter, containsk_inter, len1, min1, max1, containsk1),
                        k1 == k + 1)
    ic_consequent = inv1(k1, N, len1, min1, max1, containsk1)
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
    # CHC Rule: (=> (and (inv1...) (not (< k N)) ... (find...) (not (= ret1 k1))) fail))
    correct_condition = (ret1 == k1)
    ic_antecedent = And(inv1(k, N, len_var, min_var, max_var, containsk),
                        is_valid(containsk),
                        Not(k < N),
                        k1 >= 0,
                        k1 < N,
                        find(k1, len_var, min_var, max_var, containsk, ret1),
                        (correct_condition))
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