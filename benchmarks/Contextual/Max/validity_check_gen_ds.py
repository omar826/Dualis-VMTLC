from z3 import *

# Define variables
lmax = Int('lmax')
lmax1 = Int('lmax1')
gmax = Int('gmax')
gmax1 = Int('gmax1')
len = Int('len')
len1 = Int('len1')
v = Int('v')
v1 = Int('v1')

INT_MAX = 128
INT_MIN = -129

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

chckval = 1

# Create solver
s = Solver()

def chk_val_initial_conditions():
    global chckval
    print("===================================================")
    print("Checking if initial conditions imply loop invariant")
    print("===================================================")

    ic_antecedent = And(
        gmax1 == INT_MIN,
        lmax1 == INT_MIN,
        len1 == 0
    )
    ic_consequent = inv(lmax1, gmax1, len1)

    print("Consequent :", ic_consequent)
    ic_implication = Implies(ic_antecedent, ic_consequent)

    s.push()
    print("\nAntecedent:", ic_antecedent)
    s.add(ic_antecedent)

    print("Checking if antecedent is satisfiable:")
    if s.check() == sat:
        print("Antecedent is satisfiable")
        print("model:", s.model())
    else:
        print("Antecedent is always false")
    s.pop()

    s.push()
    print("\nImplication:", ic_implication)
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

    s.push()
    print("\nConsequent:", ic_consequent)
    s.add(ic_consequent)
    print("Checking if consequent is satisfiable:")
    if s.check() == sat:
        print("Consequent is satisfiable")
        print("model:", s.model())
    else:
        print("Consequent is always false")
    s.pop()

def chk_val_invariant1():
    global chckval
    print("===================================")
    print("Checking for loop inductiveness - 1")
    print("===================================")

    ic_antecedent = And(
        inv(lmax, gmax, len),
        append(v1, lmax, lmax1, len, len1),
        If(v1 > gmax, gmax1 == v1, gmax1 == gmax)
    )
    ic_consequent = inv(lmax1, gmax1, len1)
    ic_implication = Implies(ic_antecedent, ic_consequent)

    s.push()
    print("\nAntecedent:", ic_antecedent)
    s.add(ic_antecedent)
    print("Checking if antecedent is satisfiable:")
    if s.check() == sat:
        print("Antecedent is satisfiable")
        print("model:", s.model())
    else:
        print("Antecedent is always false")
    s.pop()

    s.push()
    print("\nImplication:", ic_implication)
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

    s.push()
    print("\nConsequent:", ic_consequent)
    s.add(ic_consequent)
    print("Checking if consequent is satisfiable:")
    if s.check() == sat:
        print("Consequent is satisfiable")
        print("model:", s.model())
    else:
        print("Consequent is always false")
    s.pop()


def chk_post():
    global chckval
    print("====================")
    print("    Checking post   ")
    print("====================")

    ic_antecedent = And(
        inv(lmax, gmax, len),
        Not(Or(len == 0, Implies(len > 0, gmax == lmax)))
    )
    ic_consequent = fail()
    ic_implication = Implies(ic_antecedent, ic_consequent)

    s.push()
    print("\nAntecedent:", ic_antecedent)
    s.add(ic_antecedent)
    print("Checking if antecedent is satisfiable:")
    if s.check() == sat:
        print("Antecedent is satisfiable")
        print("model:", s.model())
    else:
        print("Antecedent is always false")
    s.pop()

    s.push()
    print("\nImplication:", ic_implication)
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

    s.push()
    print("\nConsequent:", ic_consequent)
    s.add(ic_consequent)
    print("Checking if consequent is satisfiable:")
    if s.check() == sat:
        print("Consequent is satisfiable")
        print("model:", s.model())
    else:
        print("Consequent is always false")
    s.pop()


chk_val_initial_conditions()
chk_val_invariant1()
chk_post()

if chckval == 1:
    print("qwertyasdfg")  # Placeholder for further actions if checks fail
