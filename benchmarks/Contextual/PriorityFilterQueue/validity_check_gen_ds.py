from z3 import *

# Define variables from CHC
len = Int('len')
len1 = Int('len1')
minPrio = Int('minPrio')
minPrio1 = Int('minPrio1')
maxPacketSize = Int('maxPacketSize')
maxPacketSize1 = Int('maxPacketSize1')
packetSize = Int('packetSize')
prio = Int('prio')

# Global flag to track if all checks pass
chckval = 1

try:
    from llm_definitions import inv, append, processQueue
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
    print("="*48)
    print("Checking if initial conditions imply loop invariant")
    print("="*48)
    # CHC Rule: (=> (and (= len 0) (= minPrio 1) (= maxPacketSize 499)) (inv len minPrio maxPacketSize))
    ic_antecedent = And(len == 0, minPrio == 1, maxPacketSize == 499)
    ic_consequent = inv(len, minPrio, maxPacketSize)
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

def chk_val_invariant_append():
    global chckval
    print("="*45)
    print("Checking for loop inductiveness (Append Case)")
    print("="*45)
    # CHC Rule: (=> (and (inv...) (and (= prio 1)...) (append...)) (inv...))
    ic_antecedent = And(inv(len, minPrio, maxPacketSize),
                        prio == 1, packetSize > 0, packetSize < 500,
                        append(prio, packetSize, len, minPrio, maxPacketSize, len1, minPrio1, maxPacketSize1))
    ic_consequent = inv(len1, minPrio1, maxPacketSize1)
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
    # CHC Rule: (=> (and (inv...) (not (and (= prio 1)...))) (inv...))
    ic_antecedent = And(inv(len, minPrio, maxPacketSize),
                        Not(And(prio == 1, packetSize > 0, packetSize < 500)))
    ic_consequent = inv(len, minPrio, maxPacketSize)
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
    # CHC Rule: (=> (and (inv...) (processQueue...) (not (=> (= len1 0) (...)))) fail))
    correct_condition = Implies(len1 == 0, And(minPrio1 == minPrio, maxPacketSize1 == 499))
    ic_antecedent = And(inv(len, minPrio, maxPacketSize),
                        processQueue(len, minPrio, maxPacketSize, len1, minPrio1, maxPacketSize1),
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
chk_val_invariant_append()
chk_val_invariant_skip()
chk_post()

# --- Final result ---
if chckval == 1:
    print("\nqwertyasdfg")
