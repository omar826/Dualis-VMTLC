from z3 import *

# Define variables from CHC
N = Int('N')
i = Int('i')
i1 = Int('i1')
min_var = Int('min')
min1 = Int('min1')
max_var = Int('max')
max1 = Int('max1')
isPresent = Int('isPresent')
isPresent1 = Int('isPresent1')
len_var = Int('len')
len1 = Int('len1')
ret1 = Int('ret1')
k = Int('k')

# Define constants from CHC
MAX = 128
MIN = -129

# Global flag to track if all checks pass
chckval = 1

try:
    from llm_definitions import inv1, insert, remove
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
    # CHC Rule: (=> (and (> N 0) (= min MAX) (= max MIN) (= len 0) (= isPresent 0) (= i 0)) (inv1 i N isPresent min max len))
    ic_antecedent = And(N > 0, min_var == MAX, max_var == MIN, len_var == 0, isPresent == 0, i == 0)
    ic_consequent = inv1(i, N, isPresent, min_var, max_var, len_var)
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
    # CHC Rule: (=> (and (inv1 i N isPresent min max len) (is_valid isPresent) (< i N) (insert i isPresent min max len isPresent1 min1 max1 len1) (= i1 (+ i 1))) (inv1 i1 N isPresent1 min1 max1 len1))
    ic_antecedent = And(inv1(i, N, isPresent, min_var, max_var, len_var),
                        is_valid(isPresent),
                        i < N,
                        insert(i, isPresent, min_var, max_var, len_var, isPresent1, min1, max1, len1),
                        i1 == i + 1)
    ic_consequent = inv1(i1, N, isPresent1, min1, max1, len1)
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
    # CHC Rule: (=> (and (inv1 i N isPresent min max len) (is_valid isPresent) (not (< i N)) (<= 0 k) (< k N) (remove k len len1 ret1) (not (= len1 (- len 1)))) fail))
    correct_condition = (len1 == len_var - 1)
    ic_antecedent = And(inv1(i, N, isPresent, min_var, max_var, len_var),
                        is_valid(isPresent),
                        Not(i < N),
                        k >= 0,
                        k < N,
                        remove(k, len_var, len1, ret1),
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