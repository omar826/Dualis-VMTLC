from z3 import *

# Define variables from CHC
N = Int('N')
max_var = Int('max')
max1 = Int('max1')
min_var = Int('min')
min1 = Int('min1')
len_var = Int('len')
len1 = Int('len1')
noDup = Int('noDup')
noDup1 = Int('noDup1')
i = Int('i')
i1 = Int('i1')
data = Int('data')
ret = Int('ret')



# Global flag to track if all checks pass
chckval = 1

try:
    from llm_definitions import inv1, insert, search
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
    # CHC Rule: (=> (and (> N 0) (= max MIN) (= min MAX) (= len 0) (= noDup 1) (= i 0)) (inv1 i N max min len noDup))
    ic_antecedent = And(N > 0, max_var == -129, min_var == 128, len_var == 0, noDup == 1, i == 0)
    ic_consequent = inv1(i, N, max_var, min_var, len_var, noDup)
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
    # CHC Rule: (=> (and (inv1 i N max min len noDup) (is_valid noDup) (< i N) (insert i max min len noDup max1 min1 len1 noDup1) (= i1 (+ i 1))) (inv1 i1 N max1 min1 len1 noDup1))
    ic_antecedent = And(inv1(i, N, max_var, min_var, len_var, noDup),
                        is_valid(noDup),
                        i < N,
                        insert(i, max_var, min_var, len_var, noDup, max1, min1, len1, noDup1),
                        i1 == i + 1)
    ic_consequent = inv1(i1, N, max1, min1, len1, noDup1)
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
    # CHC Rule: (=> (and (inv1 i N max min len noDup) (is_valid noDup) (not (< i N)) (>= data 0) (< data N) (search data min max len ret) (= ret 0)) fail))
    ic_antecedent = And(inv1(i, N, max_var, min_var, len_var, noDup),
                        is_valid(noDup),
                        Not(i < N),
                        data >= 0,
                        data < N,
                        search(data, min_var, max_var, len_var, ret, noDup),
                        ret == 0)
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
        print("Implication is valid (Property holds)")
    s.pop()

# --- Run all checks ---
chk_val_initial_conditions()
chk_val_invariant()
chk_post()

# --- Final result ---
if chckval == 1:
    print("\nqwertyasdfg")
