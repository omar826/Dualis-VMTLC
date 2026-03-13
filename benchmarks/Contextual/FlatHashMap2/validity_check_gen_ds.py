from z3 import *

# Define variables from CHC
N = Int('N')
i = Int('i')
i1 = Int('i1')
containsk = Int('containsk')
containsk1 = Int('containsk1')
len = Int('len')
len1 = Int('len1')
remove_count = Int('remove_count')
remove_count1 = Int('remove_count1')
k = Int('k')
v = Int('v')

# Global flag to track if all checks pass
chckval = 1

try:
    from llm_definitions import inv1, insert, remove_none
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
    # CHC Rule: (=> (and (> N 0) (= i 0) (= containsk 0) (= len 0)) (inv1 i N len containsk)))
    ic_antecedent = And(N > 0, i == 0, containsk == 0, len == 0)
    ic_consequent = inv1(i, N, len, containsk)
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
    # CHC Rule: (=> (and (inv1...) (is_valid...) (< i N) (= k i) (= v i) (insert...) (= i1 (+ i 1))) (inv1...))
    ic_antecedent = And(inv1(i, N, len, containsk), is_valid(containsk), i < N,
                        k == i, v == i,
                        insert(k, v, len, containsk, len1, containsk1),
                        i1 == i + 1)
    ic_consequent = inv1(i1, N, len1, containsk1)
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
    # CHC Rule: (=> (and (inv1...) (not (< i N)) ... (remove_none...) (not (and (= remove_count1 0) (= len N)))) fail))
    correct_condition = And(remove_count1 == 0, len == N)
    ic_antecedent = And(inv1(i, N, len, containsk), is_valid(containsk), Not(i < N),
                        remove_count == 0,
                        remove_none(len, remove_count, len1, remove_count1),
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