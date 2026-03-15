from z3 import *

# Define variables from CHC
N = Int('N')
len_var = Int('len')
len1 = Int('len1')
i = Int('i')
i1 = Int('i1')
i_old = Int('i_old')
min_var = Int('min')
min1 = Int('min1')
max_var = Int('max')
max1 = Int('max1')
containsk = Int('containsk')
containsk1 = Int('containsk1')
k = Int('k')
v = Int('v')

# Define constants from CHC
MAX = 128
MIN = -129

# Global flag to track if all checks pass
chckval = 1

try:
    # Note: The CHC uses 'insert' and 'insert1'. Both must be defined.
    from llm_definitions import inv1, inv2, insert, insert1
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
    print("Checking if initial conditions imply first loop invariant")
    print("="*53)
    # CHC Rule: (=> (and (> N 0) (= len 0) (= i 0) (= min MIN) (= max MAX) (= containsk 0)) (inv1 i N len min max containsk))
    ic_antecedent = And(N > 0, len_var == 0, i == 0, min_var == MAX, max_var == MIN, containsk == 0)
    ic_consequent = inv1(i, N, len_var, min_var, max_var, containsk)
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
    print("="*40)
    print("Checking for first loop inductiveness")
    print("="*40)
    # CHC Rule: (=> (and (inv1...) (< i N) (insert...) (= i1 (+ i 1))) (inv1...))
    ic_antecedent = And(inv1(i, N, len_var, min_var, max_var, containsk), is_valid(containsk), i < N,
                        k == i, v == i,
                        insert(k, v, len_var, min_var, max_var, containsk, len1, min1, max1, containsk1),
                        i1 == i + 1)
    ic_consequent = inv1(i1, N, len1, min1, max1, containsk1)
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

def chk_val_transition():
    global chckval
    print("="*51)
    print("Checking transition from first loop to second loop")
    print("="*51)
    # CHC Rule: (=> (and (inv1 i_old...) (not (< i_old N)) (= i 0)) (inv2...))
    ic_antecedent = And(inv1(i_old, N, len_var, min_var, max_var, containsk), is_valid(containsk), Not(i_old < N), i == 0)
    ic_consequent = inv2(i, N, len_var, min_var, max_var, containsk)
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

def chk_val_invariant2():
    global chckval
    print("="*41)
    print("Checking for second loop inductiveness")
    print("="*41)
    # CHC Rule: (=> (and (inv2...) (< i N) (insert1...) (= i1 (+ i 1))) (inv2...))
    ic_antecedent = And(inv2(i, N, len_var, min_var, max_var, containsk), is_valid(containsk), i < N,
                        k == i, v == i,
                        insert1(k, v, len_var, min_var, max_var, containsk, len1, min1, max1, containsk1),
                        i1 == i + 1)
    ic_consequent = inv2(i1, N, len1, min1, max1, containsk1)
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
    # CHC Rule: (=> (and (inv2...) (not (< i N)) (not (= len N))) fail))
    correct_condition = (len_var == N)
    ic_antecedent = And(inv2(i, N, len_var, min_var, max_var, containsk),
                        is_valid(containsk),
                        Not(i < N),
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
        print("Implication is valid (Property holds)")
    s.pop()

# --- Run all checks ---
chk_val_initial_conditions()
chk_val_invariant1()
chk_val_transition()
chk_val_invariant2()
chk_post()

# --- Final result ---
if chckval == 1:
    print("\nqwertyasdfg")