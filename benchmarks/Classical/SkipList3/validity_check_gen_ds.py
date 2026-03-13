from z3 import *

# Define constants from CHC
MAX = 128
MIN = -129

# Define variables from CHC
N = Int('N')
i = Int('i')
i1 = Int('i1')
min = Int('min')
min1 = Int('min1')
max = Int('max')
max1 = Int('max1')
isPresent = Int('isPresent')
isPresent1 = Int('isPresent1')
len = Int('len')
len1 = Int('len1')
v = Int('v')
lb_ret1 = Int('lb_ret1')

# Global flag to track if all checks pass
chckval = 1

try:
    from llm_definitions import inv1, insert, lower_bound
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
    print("="*48)
    print("Checking if initial conditions imply loop invariant")
    print("="*48)
    # CHC Rule: (=> (and (> N 0) (= min MAX) (= max MIN) (= len 0) (= isPresent 0) (= i 0)) (inv1 i N isPresent min max len)))
    ic_antecedent = And(N > 0, min == MAX, max == MIN, len == 0, isPresent == 0, i == 0)
    ic_consequent = inv1(i, N, isPresent, min, max, len)
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

def chk_val_invariant1():
    global chckval
    print("="*36)
    print("Checking for loop inductiveness")
    print("="*36)
    # CHC Rule: (=> (and (inv1...) (is_valid...) (< i N) (insert v ...) (= i1 (+ i 1))) (inv1...))
    ic_antecedent = And(inv1(i, N, isPresent, min, max, len), is_valid(isPresent), i < N,
                        insert(v, isPresent, min, max, len, isPresent1, min1, max1, len1),
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
    # CHC Rule: (=> (and (inv1...) (not (< i N)) (lower_bound min lb_ret1) (not (>= lb_ret1 min))) fail))
    correct_condition = (lb_ret1 >= min)
    ic_antecedent = And(inv1(i, N, isPresent, min, max, len), is_valid(isPresent), Not(i < N),
                        lower_bound(min, lb_ret1),
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
chk_val_invariant1()
chk_post()

# --- Final result ---
if chckval == 1:
    print("\nqwertyasdfg")