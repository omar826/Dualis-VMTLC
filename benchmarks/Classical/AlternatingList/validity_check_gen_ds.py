from z3 import *

# Define variables from CHC
flag = Int('flag')
flag1 = Int('flag1')
top = Int('top')
top1 = Int('top1')
len_var = Int('len')
len1 = Int('len1')
val = Int('val')
val1 = Int('val1')

# Define constants from CHC
MAX = 10

# Global flag to track if all checks pass
chckval = 1

try:
    from llm_definitions import inv, push
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
    # CHC Rule: (=> (and (= flag 1) (= len 0) (= top MAX) ) (inv val top len flag))
    ic_antecedent = And(flag1 == 1, len1 == 0, top1 == MAX)
    ic_consequent = inv(val1, top1, len1, flag1)
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
    print("Checking for loop inductiveness - 1")
    print("="*40)
    # CHC Rule: (=> (and (inv val top len flag) (not (= flag 0)) (= val1 1) (push val1 top len top1 len1) (= flag1 0)) (inv val1 top1 len1 flag1))
    ic_antecedent = And(inv(val, top, len_var, flag),
                        flag != 0,
                        val1 == 1,
                        push(val1, top, len_var, top1, len1),
                        flag1 == 0)
    ic_consequent = inv(val1, top1, len1, flag1)
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
    print("="*40)
    print("Checking for loop inductiveness - 2")
    print("="*40)
    # CHC Rule: (=> (and (inv val top len flag) (= flag 0) (= val1 2) (push val1 top len top1 len1) (= flag1 1)) (inv val1 top1 len1 flag1))
    ic_antecedent = And(inv(val, top, len_var, flag),
                        flag == 0,
                        val1 == 2,
                        push(val1, top, len_var, top1, len1),
                        flag1 == 1)
    ic_consequent = inv(val1, top1, len1, flag1)
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
    # CHC Rule: (=> (and (inv val top len flag) (not (or (<= len 0) (and (=> (= flag 0) (= top 1)) (=> (= flag 1) (= top 2)))))) fail))
    correct_condition = Or(len_var <= 0,
                           And(Implies(flag == 0, top == 1),
                               Implies(flag == 1, top == 2)))
    ic_antecedent = And(inv(val, top, len_var, flag),
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
chk_val_invariant2()
chk_post()

# --- Final result ---
if chckval == 1:
    print("\nqwertyasdfg")