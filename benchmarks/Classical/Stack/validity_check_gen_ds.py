from z3 import *

# Define variables
sl = Int('sl')
sl1 = Int('sl1')
c = Int('c')
c1 = Int('c1')
d = Int('d')
d1 = Int('d1')
n = Int("n")

try:
    from llm_definitions import inv1, inv2, pu, po
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

def chk_val_invariant1():
    global chckval
    print("===============================")
    print("Checking for loop-1 inductiveness")
    print("===============================")
    antecedent = And(inv1(c, n, d, sl) , 
                        (c < n), 
                        (c1 == (c + 1)), 
                        pu(n, sl, sl1))
    consequent = inv1(c1, n, d, sl1)
    implication = Implies(antecedent, consequent)

    # Check if antecedent is satisfiable
    s.push()
    print ("\nAntecedent : ", antecedent)
    s.add(antecedent)

    print("Checking if antecedent is satisfiable:")
    if s.check() == sat:
        print("Antecedent is satisfiable")
        print("model : ", s.model())
    else:
        print("Antecedent is always false")
    s.pop()

    # Check validity of implication
    s.push()
    print("\nImplication : ", implication)
    s.add(Not(implication))
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
    print("\nConsequent : ", consequent)
    s.add(consequent)
    print("Checking if consequent is satisfiable:")
    if s.check() == sat:
        print("Consequent is satisfiable")
        print("model : ", s.model())
    else:
        print("Consequent is always false")
    s.pop()

def chk_val_loop1_2():
    global chckval
    print("===============================")
    print("Checking for loop-2 inductiveness")
    print("===============================")
    antecedent = And(inv1(c, n, d, sl) , 
                        Not(c < n))
    consequent = inv2(n, d, sl1)
    implication = Implies(antecedent, consequent)

    # Check if antecedent is satisfiable
    s.push()
    print ("\nAntecedent : ", antecedent)
    s.add(antecedent)

    print("Checking if antecedent is satisfiable:")
    if s.check() == sat:
        print("Antecedent is satisfiable")
        print("model : ", s.model())
    else:
        print("Antecedent is always false")
    s.pop()

    # Check validity of implication
    s.push()
    print("\nImplication : ", implication)
    s.add(Not(implication))
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
    print("\nConsequent : ", consequent)
    s.add(consequent)
    print("Checking if consequent is satisfiable:")
    if s.check() == sat:
        print("Consequent is satisfiable")
        print("model : ", s.model())
    else:
        print("Consequent is always false")
    s.pop()

def chk_val_invariant2():
    global chckval
    print("===============================")
    print("Checking for loop-2 inductiveness")
    print("===============================")
    antecedent = And(inv2(n, d, sl) , 
                        (sl == 0),
                        Not (sl == 0),
                        po(sl, sl1),
                        (d1 == d + 1)
                        )
    consequent = inv2(n, d1, sl1)
    implication = Implies(antecedent, consequent)

    # Check if antecedent is satisfiable
    s.push()
    print ("\nAntecedent : ", antecedent)
    s.add(antecedent)

    print("Checking if antecedent is satisfiable:")
    if s.check() == sat:
        print("Antecedent is satisfiable")
        print("model : ", s.model())
    else:
        print("Antecedent is always false")
    s.pop()

    # Check validity of implication
    s.push()
    print("\nImplication : ", implication)
    s.add(Not(implication))
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
    print("\nConsequent : ", consequent)
    s.add(consequent)
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
    antecedent = And(
                    inv2(n, d, sl),
                    (sl == 0),
                    (d != n)
    )
    consequent = fail()
    implication = Implies(antecedent, consequent)

    # Check if antecedent is satisfiable
    s.push()
    print ("\nAntecedent : ", antecedent)
    s.add(antecedent)

    print("Checking if antecedent is satisfiable:")
    if s.check() == sat:
        print("Antecedent is satisfiable")
        print("model : ", s.model())
    else:
        print("Antecedent is always false")
    s.pop()

    # Check validity of implication
    s.push()
    print("\nImplication : ", implication)
    s.add(Not(implication))
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
    print("\nConsequent : ", consequent)
    s.add(consequent)
    print("Checking if consequent is satisfiable:")
    if s.check() == sat:
        print("Consequent is satisfiable")
        print("model : ", s.model())
    else:
        print("Consequent is always false")
    s.pop()

    
def chk_val_initial_conditions():
    global chckval
    print("===================================================")
    print("Checking if initial conditions imply loop invariant")
    print("===================================================")
    # initial conditions
    antecedent = And((n > 0),
                    (sl == 0),
                    (c == 0),
                    (d == 0))
    consequent = inv1(c, n, d, sl)
    implication = Implies(antecedent, consequent)

    # Check if antecedent is satisfiable
    s.push()
    print ("\nAntecedent : ", antecedent)
    s.add(antecedent)
    print("Checking if antecedent is satisfiable:")
    if s.check() == sat:
        print("Antecedent is satisfiable")
        print("model : ", s.model())
    else:
        print("Antecedent is always false")
    s.pop()

    # Check validity of implication
    s.push()
    print("\nImplication : ", implication)
    s.add(Not(implication))
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
    print("\nConsequent : ", consequent)
    s.add(consequent)
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