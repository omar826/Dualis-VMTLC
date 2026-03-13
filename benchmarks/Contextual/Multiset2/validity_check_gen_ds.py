from z3 import *

# Define variables from CHC
N = Int('N')
v = Int('v')
v1 = Int('v1')
i = Int('i')
i1 = Int('i1')
countvo = Int('countvo')
countvo1 = Int('countvo1')
countvt = Int('countvt')
countvt1 = Int('countvt1')
len_var = Int('len')
len1 = Int('len1')

# Global flag to track if all checks pass
chckval = 1

try:
    from llm_definitions import inv1, emplace, emplace1
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
    print("="*53)
    print("Checking if initial conditions imply loop invariant")
    print("="*53)
    # CHC Rule: (=> (and (> N 0) (= v 1) (= i 0) (= countvo 0) (= countvt 0) (= len 0)) (inv1 i N v countvo countvt len))
    ic_antecedent = And(N > 0, v == 1, i == 0, countvo == 0, countvt == 0, len_var == 0)
    ic_consequent = inv1(i, N, v, countvo, countvt, len_var)
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
    # CHC Rule: (=> (and (inv1 i N v countvo countvt len) (< i N) (emplace v countvo countvt len countvo1 countvt1 len1) (= i1 (+ i 1))) (inv1 i1 N v countvo1 countvt1 len1))
    ic_antecedent = And(inv1(i, N, v, countvo, countvt, len_var),
                        i < N,
                        emplace(v, countvo, countvt, len_var, countvo1, countvt1, len1),
                        i1 == i + 1)
    ic_consequent = inv1(i1, N, v, countvo1, countvt1, len1)
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
    # CHC Rule: (=> (and (inv1 i N v countvo countvt len) (not (< i N)) (= v1 2) (emplace1 ...) (not (and (= len1 (+ N 1)) (= countvt1 1)))) fail))
    correct_condition = And(len1 == N + 1, countvt1 == 1)
    ic_antecedent = And(inv1(i, N, v, countvo, countvt, len_var),
                        Not(i < N),
                        v1 == 2,
                        emplace1(v1, countvo, countvt, len_var, countvo1, countvt1, len1),
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