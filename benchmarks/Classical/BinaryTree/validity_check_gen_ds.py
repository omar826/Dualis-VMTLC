from z3 import *

from globals import *

# INT_MAX = 32767 (Globally available Python constant as per Section III)

chckval = 1

try:
    from llm_definitions import inv, insert, search
    print("Successfully imported definitions from llm_definitions.py")
except ImportError:
    print("ERROR: Could not import from 'llm_definitions.py'.")
    print("Please run 'prompt_and_generate.py' first to create this file.")
    exit() # Stop the script if the definitions aren't available
except Exception as e:
    print(f"An error occurred during import: {e}")
    exit()
# (declare-rel fail ())
def fail():
    return z3.BoolVal(False)  # This relation always returns False, indicating failure.

# Create a single solver
s = Solver()

def chk_val_initial_conditions():
    global chckval
    print("===================================================")
    print("Checking if initial conditions imply loop invariant")
    print("===================================================")
    # initial conditions
    ic_antecedent = And(isEmpty1 == True,min1 == INT_MAX)
    ic_consequent = inv(min1, isEmpty1, n)
    print("Consequent : ", ic_consequent)
    ic_implication = Implies(ic_antecedent, ic_consequent)

    # Check if antecedent is satisfiable
    s.push()
    print ("\nAntecedent : ", ic_antecedent)
    s.add(ic_antecedent)

    print("Checking if antecedent is satisfiable:")
    if s.check() == sat:
        print("Antecedent is satisfiable")
        print("model : ", s.model())
    else:
        print("Antecedent is always false")
    s.pop()

    # Check validity of implication
    s.push()
    print("\nImplication : ", ic_implication)
    s.add(Not(ic_implication))
    print(s.assertions())
    print("Checking validity of implication:")
    if s.check() == sat:
        print("Counterexample found (Implication is not valid):")
        print(s.model())
        chckval = 0
    else:
        print("Implication is valid")
    s.pop()

    # Check if consequent is satisfiable
    s.push()
    print("\nConsequent : ", ic_consequent)
    s.add(ic_consequent)
    print("Checking if consequent is satisfiable:")
    if s.check() == sat:
        print("Consequent is satisfiable")
        print("model : ", s.model())
    else:
        print("Consequent is always false")
    s.pop()

def chk_val_invariant1():
    global chckval
    print("===================================")
    print("Checking for loop inductiveness - 1")
    print("===================================")
    ic_antecedent = And(
        inv(min, isEmpty, n),
        (n1 >= 0),
        insert(n1, min, min1, isEmpty, isEmpty1))
    ic_consequent = inv(min1, isEmpty1, n1)
    ic_implication = Implies(ic_antecedent, ic_consequent)

    # Check if antecedent is satisfiable
    s.push()
    print ("\nAntecedent : ", ic_antecedent)
    s.add(ic_antecedent)

    print("Checking if antecedent is satisfiable:")
    if s.check() == sat:
        print("Antecedent is satisfiable")
        print("model : ", s.model())
    else:
        print("Antecedent is always false")
    s.pop()

    # Check validity of implication
    s.push()
    print("\nImplication : ", ic_implication)
    s.add(Not(ic_implication))
    print(s.assertions())
    print("Checking validity of implication:")
    if s.check() == sat:
        print("Counterexample found (Implication is not valid):")
        print(s.model())
        chckval = 0
    else:
        print("Implication is valid")
    s.pop()

    # Check if consequent is satisfiable
    s.push()
    print("\nConsequent : ", ic_consequent)
    s.add(ic_consequent)
    print("Checking if consequent is satisfiable:")
    if s.check() == sat:
        print("Consequent is satisfiable")
        print("model : ", s.model())
    else:
        print("Consequent is always false")
    s.pop()

def chk_val_invariant2():
    global chckval
    print("===================================")
    print("Checking for loop inductiveness - 2")
    print("===================================")
    ic_antecedent = And(
        inv(min, isEmpty, n),
        (n1 < 0))
    ic_consequent = inv(min, isEmpty, n1)
    ic_implication = Implies(ic_antecedent, ic_consequent)

    # Check if antecedent is satisfiable
    s.push()
    print ("\nAntecedent : ", ic_antecedent)
    s.add(ic_antecedent)

    print("Checking if antecedent is satisfiable:")
    if s.check() == sat:
        print("Antecedent is satisfiable")
        print("model : ", s.model())
    else:
        print("Antecedent is always false")
    s.pop()

    # Check validity of implication
    s.push()
    print("\nImplication : ", ic_implication)
    s.add(Not(ic_implication))
    print(s.assertions())
    print("Checking validity of implication:")
    if s.check() == sat:
        print("Counterexample found (Implication is not valid):")
        print(s.model())
        chckval = 0
    else:
        print("Implication is valid")
    s.pop()

    # Check if consequent is satisfiable
    s.push()
    print("\nConsequent : ", ic_consequent)
    s.add(ic_consequent)
    print("Checking if consequent is satisfiable:")
    if s.check() == sat:
        print("Consequent is satisfiable")
        print("model : ", s.model())
    else:
        print("Consequent is always false")
    s.pop()

def chk_post():
    global chckval
    print("====================")
    print("    Checking post   ")
    print("====================")
    ic_antecedent = And(
        inv(min, isEmpty, n),
        (v < 0),
        search(v, min, isEmpty, ret1),
        (ret1 == True)
    )
    ic_consequent = fail()
    ic_implication = Implies(ic_antecedent, ic_consequent)

    # Check if antecedent is satisfiable
    s.push()
    print ("\nAntecedent : ", ic_antecedent)
    s.add(ic_antecedent)

    print("Checking if antecedent is satisfiable:")
    if s.check() == sat:
        print("Antecedent is satisfiable")
        print("model : ", s.model())
    else:
        print("Antecedent is always false")
    s.pop()

    # Check validity of implication
    s.push()
    print("\nImplication : ", ic_implication)
    s.add(Not(ic_implication))
    print(s.assertions())
    print("Checking validity of implication:")
    if s.check() == sat:
        print("Counterexample found (Implication is not valid):")
        print(s.model())
        chckval = 0
    else:
        print("Implication is valid")
    s.pop()

    # Check if consequent is satisfiable
    s.push()
    print("\nConsequent : ", ic_consequent)
    s.add(ic_consequent)
    print("Checking if consequent is satisfiable:")
    if s.check() == sat:
        print("Consequent is satisfiable")
        print("model : ", s.model())
    else:
        print("Consequent is always false")
    s.pop()

chk_val_initial_conditions()
chk_val_invariant1()
chk_val_invariant2()
chk_post()


if chckval == 1:
    print("qwertyasdfg")




