from z3 import *

# Define variables from CHC
len_var = Int('len')
len1 = Int('len1')
ev1 = Int('ev1')
ev2 = Int('ev2')
maxDiff = Int('maxDiff')
maxDiff1 = Int('maxDiff1')

# Define constants from CHC
INT_MIN = 0

# Global flag to track if all checks pass
chckval = 1

try:
    from llm_definitions import inv, insert
    print("Successfully imported definitions from llm_definitions.py")
except ImportError:
    print("ERROR: Could not import from 'llm_definitions.py'.")
    exit()
except Exception as e:
    print(f"An error occurred during import: {e}")
    exit()

def absl(x):
    """CHC Helper: (define-fun absl ((x Int)) Int (ite (>= x 0) x (- x)))"""
    return If(x >= 0, x, -x)

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
    # CHC Rule: (=> (and (= len1 0) (= INT_MIN maxDiff1)) (inv len1 maxDiff1))
    ic_antecedent = And(len1 == 0, maxDiff1 == INT_MIN)
    ic_consequent = inv(len1, maxDiff1)
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

def chk_val_invariant_insert():
    global chckval
    print("="*45)
    print("Checking for loop inductiveness (Insert Case)")
    print("="*45)
    # CHC Rule: (=> (and (inv len maxDiff) (>= ev1 0) ... (< (absl (- ev1 ev2)) 2) (insert ...)) (inv len1 maxDiff1))
    ic_antecedent = And(inv(len_var, maxDiff),
                        ev1 >= 0, ev1 <= 3,
                        ev2 >= 0, ev2 <= 3,
                        absl(ev1 - ev2) < 2,
                        insert(len_var, len1, ev1, ev2, maxDiff, maxDiff1))
    ic_consequent = inv(len1, maxDiff1)
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

def chk_val_invariant_skip():
    global chckval
    print("="*44)
    print("Checking for loop inductiveness (Skip Case)")
    print("="*44)
    # CHC Rule: (=> (and (inv len maxDiff) (not (and ...))) (inv len maxDiff))
    skip_condition = And(ev1 >= 0, ev1 <= 3,
                         ev2 >= 0, ev2 <= 3,
                         absl(ev1 - ev2) < 2)
    ic_antecedent = And(inv(len_var, maxDiff), Not(skip_condition))
    ic_consequent = inv(len_var, maxDiff)
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
    # CHC Rule: (=> (and (inv len maxDiff) (not (=> (> len 0)(< maxDiff 2)))) fail))
    correct_condition = Implies(len_var > 0, maxDiff < 2)
    ic_antecedent = And(inv(len_var, maxDiff), Not(correct_condition))
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
chk_val_invariant_insert()
chk_val_invariant_skip()
chk_post()

# --- Final result ---
if chckval == 1:
    print("\nqwertyasdfg")