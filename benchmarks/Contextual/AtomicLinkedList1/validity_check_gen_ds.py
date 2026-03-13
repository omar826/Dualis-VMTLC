from z3 import *

# Define variables
N = Int('N')
k = Int('k')
k1 = Int('k1')
len = Int('len')
len1 = Int('len1')
items_processed = Int('items_processed')
items_processed1 = Int('items_processed1')
ret1 = Int('ret1')

chckval = 1

try:
    from llm_definitions import inv1, inv2, insertHead, popHead
    print("Successfully imported definitions from llm_definitions.py")
except ImportError:
    print("ERROR: Could not import from 'llm_definitions.py'.")
    exit() # Stop the script if the definitions aren't available
except Exception as e:
    print(f"An error occurred during import: {e}")
    exit()


def fail():
    return BoolVal(False)

# Create a single solver
s = Solver()

def chk_val_initial_conditions1():
    global chckval
    print("==========================================================")
    print("Checking if initial conditions imply first loop invariant")
    print("==========================================================")
    # CHC Rule: (=> (and (> N 0) (= k1 0) (= len1 0)) (inv1 k1 N len1))
    ic_antecedent = And(N > 0, k1 == 0, len1 == 0)
    ic_consequent = inv1(k1, N, len1)
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
        chckval = 0
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

def chk_val_invariant1():
    global chckval
    print("==========================================")
    print("Checking for first loop inductiveness")
    print("==========================================")
    # CHC Rule: (=> (and (inv1 k N len) (< k N) (insertHead k len len1) (= k1 (+ k 1))) (inv1 k1 N len1))
    ic_antecedent = And(inv1(k, N, len),
                        k < N,
                        insertHead(k, len, len1),
                        k1 == k + 1)
    ic_consequent = inv1(k1, N, len1)
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
        chckval = 0
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

def chk_val_transition():
    global chckval
    print("=====================================================")
    print("Checking transition from first loop to second loop")
    print("=====================================================")
    # CHC Rule: (=> (and (inv1 k N len) (not (< k N)) (= items_processed 0)) (inv2 len items_processed N))
    ic_antecedent = And(inv1(k, N, len),
                        Not(k < N),
                        items_processed == 0)
    ic_consequent = inv2(len, items_processed, N)
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
        chckval = 0
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

def chk_val_invariant2():
    global chckval
    print("==========================================")
    print("Checking for second loop inductiveness")
    print("==========================================")
    # CHC Rule: (=> (and (inv2 len items_processed N) (not (= len 0)) (popHead len ret1 len1) (= items_processed1 (+ items_processed 1))) (inv2 len1 items_processed1 N))
    ic_antecedent = And(inv2(len, items_processed, N),
                        len != 0,
                        popHead(len, ret1, len1),
                        items_processed1 == items_processed + 1)
    ic_consequent = inv2(len1, items_processed1, N)
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
        chckval = 0
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

def chk_post():
    global chckval
    print("====================")
    print("   Checking post   ")
    print("====================")
    # CHC Rule: (=> (and (inv2 len items_processed N) (= len 0) (not (= items_processed N))) fail))
    correct_condition = (items_processed == N)
    ic_antecedent = And(inv2(len, items_processed, N),
                        len == 0,
                        Not(correct_condition))
    ic_consequent = fail()
    ic_implication = Implies(ic_antecedent, ic_consequent)

    s.push()
    print("\nAntecedent : ", ic_antecedent)
    s.add(ic_antecedent)
    print("Checking if antecedent is satisfiable:")
    if s.check() == sat:
        print("Antecedent is satisfiable (potential violation):")
        print("Model : ", s.model())
    else:
        print("Antecedent is not satisfiable (property holds)")
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
        print("Implication is valid (property holds)")
    s.pop()


chk_val_initial_conditions1()
chk_val_invariant1()
chk_val_transition()
chk_val_invariant2()
chk_post()

if chckval == 1:
    print("qwertyasdfg")