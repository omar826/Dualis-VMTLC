from z3 import *

# Define variables
val = Int('val')
min = Int('min')
min1 = Int('min1')
max = Int('max')
max1 = Int('max1')

try:
    from llm_definitions import inv, push
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

chckval = 1  # Global variable to track validity of checks

# Create a single solver
s = Solver()

def chk_initial_conditions():
    global chckval
    print("===================================================")
    print("Checking if initial conditions imply loop invariant")
    print("===================================================")

    ic_antecedent = And(min == 0, max == 0, val == 0)
    ic_consequent = inv(val, min, max)
    ic_implication = Implies(ic_antecedent, ic_consequent)

    s.push()
    print("\nAntecedent : ", ic_antecedent)
    s.add(ic_antecedent)
    print("Checking if antecedent is satisfiable:")
    if s.check() == sat:
        print("Antecedent is satisfiable")
        print("Model : ", s.model())
    else:
        print("Antecedent is always false")
    s.pop()

    s.push()
    print("\nImplication : ", ic_implication)
    s.add(Not(ic_implication))
    print("Checking validity of implication:")
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
    print("Checking if consequent is satisfiable:")
    if s.check() == sat:
        print("Consequent is satisfiable")
        print("Model : ", s.model())
    else:
        print("Consequent is always false")
    s.pop()

def chk_invariant_preservation():
    global chckval
    print("===================================")
    print("Checking for loop inductiveness")
    print("===================================")

    antecedent = And(inv(val, min, max), push(val, min, min1, max, max1))
    consequent = inv(val, min1, max1)
    implication = Implies(antecedent, consequent)

    s.push()
    print("\nAntecedent : ", antecedent)
    s.add(antecedent)
    print("Checking if antecedent is satisfiable:")
    if s.check() == sat:
        print("Antecedent is satisfiable")
        print("Model : ", s.model())
    else:
        print("Antecedent is always false")
    s.pop()

    s.push()
    print("\nImplication : ", implication)
    s.add(Not(implication))
    print("Checking validity of implication:")
    if s.check() == sat:
        print("Counterexample found (Implication is not valid):")
        print("Model : ", s.model())
        chckval = 0
    else:
        print("Implication is valid")
    s.pop()

    s.push()
    print("\nConsequent : ", consequent)
    s.add(consequent)
    print("Checking if consequent is satisfiable:")
    if s.check() == sat:
        print("Consequent is satisfiable")
        print("Model : ", s.model())
    else:
        print("Consequent is always false")
    s.pop()

def chk_post_condition():
    global chckval
    print("====================")
    print("    Checking post   ")
    print("====================")

    antecedent = And(inv(val, min, max), Not(And(min == 0, max == 0)))
    consequent = fail()
    implication = Implies(antecedent, consequent)

    s.push()
    print("\nAntecedent : ", antecedent)
    s.add(antecedent)
    print("Checking if antecedent is satisfiable:")
    if s.check() == sat:
        print("Antecedent is satisfiable")
        print("Model : ", s.model())
    else:
        print("Antecedent is always false")
    s.pop()

    s.push()
    print("\nImplication : ", implication)
    s.add(Not(implication))
    print("Checking validity of implication:")
    if s.check() == sat:
        print("Counterexample found (Implication is not valid):")
        print("Model : ", s.model())
        chckval = 0
    else:
        print("Implication is valid")
    s.pop()


chk_initial_conditions()
chk_invariant_preservation()
chk_post_condition()

if chckval == 1:
    print("qwertyasdfg")  # Placeholder for further actions if checks fail