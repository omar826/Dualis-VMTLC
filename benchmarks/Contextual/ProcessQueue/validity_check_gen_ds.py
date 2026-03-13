from z3 import *

# Define variables from CHC
nexttime = Int('nexttime')
len_var = Int('len')
min_ttw = Int('min_ttw')
nexttime1 = Int('nexttime1')
len1 = Int('len1')
min_ttw1 = Int('min_ttw1')

# Define constants from CHC
MAX = 128
MIN = -129

# Global flag to track if all checks pass
chckval = 1

try:
    from llm_definitions import inv, insert, choosenext
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
    # CHC Rule: (=> (and (= len1 0) (= nexttime1 1) (= min_ttw1 INT_MAX)) (inv nexttime1 len1 min_ttw1))
    ic_antecedent = And(len1 == 0, nexttime1 == 1, min_ttw1 == MAX)
    ic_consequent = inv(nexttime1, len1, min_ttw1)
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

def chk_invariant_insert():
    global chckval
    print("="*44)
    print("Checking for loop inductiveness (Insert Case)")
    print("="*44)
    # CHC Rule: (=> (and (inv nexttime len min_ttw) (insert nexttime len len1 min_ttw min_ttw1) (= nexttime1 (+ nexttime 1))) (inv nexttime1 len1 min_ttw1))
    ic_antecedent = And(inv(nexttime, len_var, min_ttw),
                        insert(nexttime, len_var, len1, min_ttw, min_ttw1),
                        nexttime1 == nexttime + 1)
    ic_consequent = inv(nexttime1, len1, min_ttw1)
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

def chk_invariant_choosenext():
    global chckval
    print("="*49)
    print("Checking for loop inductiveness (ChooseNext Case)")
    print("="*49)
    # CHC Rule: (=> (and (inv nexttime len min_ttw) (and (> nexttime 1) (choosenext len len1 min_ttw min_ttw1) (= nexttime1 (- nexttime 1)))) (inv nexttime1 len1 min_ttw1))
    ic_antecedent = And(inv(nexttime, len_var, min_ttw),
                        nexttime > 1,
                        choosenext(len_var, len1, min_ttw, min_ttw1),
                        nexttime1 == nexttime - 1)
    ic_consequent = inv(nexttime1, len1, min_ttw1)
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

def chk_invariant_skip():
    global chckval
    print("="*41)
    print("Checking for loop inductiveness (Skip Case)")
    print("="*41)
    # CHC Rule: (=> (and (inv nexttime len min_ttw) (<= nexttime 1)) (inv nexttime len min_ttw))
    ic_antecedent = And(inv(nexttime, len_var, min_ttw), nexttime <= 1)
    ic_consequent = inv(nexttime, len_var, min_ttw)
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
    # CHC Rule: (=> (and (inv nexttime len min_ttw) (not(=> (> len 0) (>= min_ttw 1)))) fail))
    correct_condition = Implies(len_var > 0, min_ttw >= 1)
    ic_antecedent = And(inv(nexttime, len_var, min_ttw), Not(correct_condition))
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
chk_invariant_insert()
chk_invariant_choosenext()
chk_invariant_skip()
chk_post()

# --- Final result ---
if chckval == 1:
    print("\nqwertyasdfg")