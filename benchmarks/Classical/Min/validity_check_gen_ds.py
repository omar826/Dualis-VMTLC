from z3 import *

# Define constants
INT_MAX = 128
INT_MIN = -129

# Define variables
v = Int('v')
v1 = Int('v1')
lmin = Int('lmin')
lmin1 = Int('lmin1')
gmin = Int('gmin')
gmin1 = Int('gmin1')
len = Int('len')
len1 = Int('len1')

try:
    from llm_definitions import inv, append
    print("Successfully imported definitions from llm_definitions.py")
except ImportError:
    print("ERROR: Could not import from 'llm_definitions.py'.")
    print("Please run 'prompt_and_generate.py' first to create this file.")
    exit() # Stop the script if the definitions aren't available
except Exception as e:
    print(f"An error occurred during import: {e}")
    exit()

def fail():
    return False  # Represents a failure condition

chckval = 1  # Flag to track validity of checks

# Create a single solver
s = Solver()

def chk_val_initial_conditions():
    global chckval
    print("===================================================")
    print("Checking if initial conditions imply loop invariant")
    print("===================================================")
    ic_antecedent = And(gmin1 == INT_MAX, lmin1 == INT_MAX, len1 == 0)
    ic_consequent = inv(lmin1, gmin1, len1)
    ic_implication = Implies(ic_antecedent, ic_consequent)

    s.push()
    print("\nAntecedent : ", ic_antecedent)
    s.add(ic_antecedent)
    if s.check() == sat:
        print("Antecedent is satisfiable")
        print("Model : ", s.model())
    else:
        print("Antecedent is always false")
    s.pop()

    s.push()
    print("\nImplication : ", ic_implication)
    s.add(Not(ic_implication))
    if s.check() == sat:
        print("Counterexample found (Implication is not valid):")
        print("Model : ", s.model())
        chckval = 0
    else:
        print("Implication is valid")
    s.pop()

    s.push()
    print("\nConsequent : ", ic_consequent)
    s.add(ic_consequent)
    if s.check() == sat:
        print("Consequent is satisfiable")
        print("Model : ", s.model())
    else:
        print("Consequent is always false")
    s.pop()

def chk_val_invariant1():
    global chckval
    print("===================================")
    print("Checking for loop inductiveness - 1")
    print("===================================")
    ic_antecedent = And(
        inv(lmin, gmin, len),
        append(v1, lmin, lmin1, len, len1),
        If(gmin > v1, gmin1 == v1, gmin1 == gmin)
    )
    ic_consequent = inv(lmin1, gmin1, len1)
    ic_implication = Implies(ic_antecedent, ic_consequent)

    s.push()
    print("\nAntecedent : ", ic_antecedent)
    s.add(ic_antecedent)
    if s.check() == sat:
        print("Antecedent is satisfiable")
        print("Model : ", s.model())
    else:
        print("Antecedent is always false")
    s.pop()

    s.push()
    print("\nImplication : ", ic_implication)
    s.add(Not(ic_implication))
    if s.check() == sat:
        print("Counterexample found (Implication is not valid):")
        print("Model : ", s.model())
        chckval = 0
    else:
        print("Implication is valid")
    s.pop()

    s.push()
    print("\nConsequent : ", ic_consequent)
    s.add(ic_consequent)
    if s.check() == sat:
        print("Consequent is satisfiable")
        print("Model : ", s.model())
    else:
        print("Consequent is always false")
    s.pop()



def chk_post():
    global chckval
    print("====================")
    print("    Checking post   ")
    print("====================")
    ic_antecedent = And(
        inv(lmin, gmin, len),
        Not(Or(len == 0, Implies(len > 0, gmin == lmin)))
    )
    ic_consequent = fail()
    ic_implication = Implies(ic_antecedent, ic_consequent)

    s.push()
    print("\nAntecedent : ", ic_antecedent)
    s.add(ic_antecedent)
    if s.check() == sat:
        print("Antecedent is satisfiable")
        print("Model : ", s.model())
    else:
        print("Antecedent is always false")
    s.pop()

    s.push()
    print("\nImplication : ", ic_implication)
    s.add(Not(ic_implication))
    if s.check() == sat:
        print("Counterexample found (Implication is not valid):")
        print("Model : ", s.model())
        chckval = 0
    else:
        print("Implication is valid")
    s.pop()


chk_val_initial_conditions()
chk_val_invariant1()
chk_post()

if chckval == 1:
    print("qwertyasdfg")  # Placeholder for further actions if checks fail

