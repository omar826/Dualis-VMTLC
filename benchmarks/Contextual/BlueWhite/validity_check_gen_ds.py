from z3 import *

# Define variables from CHC
color = Int('color')
color1 = Int('color1')
inserted_blue = Int('inserted_blue')
inserted_blue1 = Int('inserted_blue1')
bcount = Int('bcount')
bcount1 = Int('bcount1')

# Global flag to track if all checks pass
chckval = 1

try:
    # Note: The CHC uses 'push1' in one rule, which is likely a typo.
    # We assume it should be 'push' and import it.
    from llm_definitions import inv, push, push1
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

def chk_initial_conditions():
    global chckval
    print("="*53)
    print("Checking if initial conditions imply loop invariant")
    print("="*53)
    # CHC Rule: (=> (and (= inserted_blue1 0) (= bcount1 0)) (inv inserted_blue1 bcount1 color)))
    ic_antecedent = And(inserted_blue1 == 0, bcount1 == 0)
    ic_consequent = inv(inserted_blue1, bcount1, color)
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

def chk_inductive_push_blue():
    global chckval
    print("="*45)
    print("Checking for loop inductiveness (Push Blue Case)")
    print("="*45)
    # CHC Rule: (=> (and (inv...) (and (= color 0) (= inserted_blue 0)) (push...) ...) (inv...))
    ic_antecedent = And(inv(inserted_blue, bcount, color),
                        color == 0,
                        inserted_blue == 0,
                        push(color, bcount, bcount1),
                        inserted_blue1 == 1)
    ic_consequent = inv(inserted_blue1, bcount1, color1)
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

def chk_inductive_push_white():
    global chckval
    print("="*46)
    print("Checking for loop inductiveness (Push White Case)")
    print("="*46)
    # CHC Rule: (=> (and (inv...) (not...) (= color 1) (push1...)) (inv...))
    # Correcting typo from push1 to push
    ic_antecedent = And(inv(inserted_blue, bcount, color),
                        Not(And(color == 0, inserted_blue == 0)),
                        color == 1,
                        push1(color, bcount, bcount1))
    ic_consequent = inv(inserted_blue, bcount1, color1)
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

def chk_inductive_skip():
    global chckval
    print("="*41)
    print("Checking for loop inductiveness (Skip Case)")
    print("="*41)
    # CHC Rule: (=> (and (inv...) (not...) (not (= color 1))) (inv...))
    ic_antecedent = And(inv(inserted_blue, bcount, color),
                        Not(And(color == 0, inserted_blue == 0)),
                        Not(color == 1))
    ic_consequent = inv(inserted_blue, bcount, color1)
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
    # CHC Rule: (=> (and (inv...) (not (=> (= inserted_blue 1) (= bcount 1)))) fail))
    correct_condition = Implies(inserted_blue == 1, bcount == 1)
    ic_antecedent = And(inv(inserted_blue, bcount, color),
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
chk_initial_conditions()
chk_inductive_push_blue()
chk_inductive_push_white()
chk_inductive_skip()
chk_post()

# --- Final result ---
if chckval == 1:
    print("\nqwertyasdfg")