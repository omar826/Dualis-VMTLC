from z3 import *

# Define variables from CHC
N = Int('N')
v = Int('v')
i = Int('i')
i1 = Int('i1')
countv = Int('countv')
countv1 = Int('countv1')
len = Int('len')
len1 = Int('len1')

# Global flag to track if all checks pass
chckval = 1

try:
    from llm_definitions import inv1, emplace
    print("Successfully imported definitions from llm_definitions.py")
except ImportError:
    print("ERROR: Could not import from 'llm_definitions.py'.")
    exit()
except Exception as e:
    print(f"An error occurred during import: {e}")
    exit()

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
    # CHC Rule: (=> (and (> N 0) (= i 0) (= countv 0) (= len 0)) (inv1 i N v countv len))
    ic_antecedent = And(N > 0, i == 0, countv == 0, len == 0)
    ic_consequent = inv1(i, N, v, countv, len)
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
    # CHC Rule: (=> (and (inv1 i N v countv len) (< i N) (emplace v countv len countv1 len1) (= i1 (+ i 1))) (inv1 i1 N v countv1 len1))
    ic_antecedent = And(inv1(i, N, v, countv, len), i < N,
                        emplace(v, countv, len, countv1, len1),
                        i1 == i + 1)
    ic_consequent = inv1(i1, N, v, countv1, len1)
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
    # CHC Rule: (=> (and (inv1 i N v countv len) (not (< i N)) (not (and (= len N) (= countv N)))) fail))
    correct_condition = And(len == N, countv == N)
    ic_antecedent = And(inv1(i, N, v, countv, len),
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