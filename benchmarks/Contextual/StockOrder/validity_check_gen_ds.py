from z3 import *

# Define constants
MAX = 128

# Define variables
stock = Int('stock')
order = Int('order')
len = Int('len')
len1 = Int('len1')
minDiff = Int('minDiff')
minDiff1 = Int('minDiff1')

try:
    from llm_definitions import inv, addStockOrder
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
    ic_antecedent = And(len1 == 0, minDiff1 == MAX)
    ic_consequent = inv(len1, minDiff1)
    ic_implication = Implies(ic_antecedent, ic_consequent)

    # Check if antecedent is satisfiable
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

    # Check validity of implication
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

    # Check if consequent is satisfiable
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

def chk_val_invariant1():
    global chckval
    print("===================================")
    print("Checking for loop inductiveness - 1")
    print("===================================")
    ic_antecedent = And(
        inv(len, minDiff),
        stock >= 0,
        order >= 0,
        order <= stock,
        addStockOrder(stock, order, len, minDiff, len1, minDiff1)
    )
    ic_consequent = inv(len1, minDiff1)
    ic_implication = Implies(ic_antecedent, ic_consequent)

    # Check if antecedent is satisfiable
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

    # Check validity of implication
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

    # Check if consequent is satisfiable
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

def chk_val_invariant2():
    global chckval
    print("===================================")
    print("Checking for loop inductiveness - 2")
    print("===================================")
    ic_antecedent = And(
        inv(len, minDiff),
        Or(stock < 0, order < 0, order > stock)
    )
    ic_consequent = inv(len, minDiff)
    ic_implication = Implies(ic_antecedent, ic_consequent)

    # Check if antecedent is satisfiable
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

    # Check validity of implication
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

    # Check if consequent is satisfiable
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

def chk_post():
    global chckval
    print("====================")
    print("    Checking post   ")
    print("====================")
    ic_antecedent = And(
        inv(len, minDiff),
        Not(Implies(len >= 0, minDiff >= 0))
    )
    ic_consequent = fail()
    ic_implication = Implies(ic_antecedent, ic_consequent)

    # Check if antecedent is satisfiable
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

    # Check validity of implication
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

# Main program execution
chk_val_initial_conditions()
chk_val_invariant1()
chk_val_invariant2()
chk_post()

if chckval == 1:
    print("qwertyasdfg")