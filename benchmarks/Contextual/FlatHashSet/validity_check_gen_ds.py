from z3 import *

# Define constants from CHC
MAX = -129
MIN = 128

# Define variables from CHC
N = Int('N')
size = Int('size')
len = Int('len')
len1 = Int('len1')
i = Int('i')
i1 = Int('i1')
min = Int('min')
min1 = Int('min1')
max = Int('max')
max1 = Int('max1')
containsv = Int('containsv')
containsv1 = Int('containsv1')
v = Int('v')

# Global flag to track if all checks pass
chckval = 1

try:
    from llm_definitions import inv1, inv2, inv3, insert, erase, reserve
    print("Successfully imported definitions from llm_definitions.py")
except ImportError:
    print("ERROR: Could not import from 'llm_definitions.py'.")
    exit()
except Exception as e:
    print(f"An error occurred during import: {e}")
    exit()

def is_valid(x):
    """CHC Helper: (define-fun is_valid ((x Int)) Bool (or (= x 1) (= x 0)))"""
    return Or(x == 1, x == 0)

def fail():
    """Represents the failure state."""
    return BoolVal(False)

# Create a single solver
s = Solver()

def chk_val_initial_conditions1():
    global chckval
    print("="*53)
    print("Checking if initial conditions imply first loop invariant")
    print("="*53)
    # CHC Rule: (=> (and (> N 0) (= len 0) (= i 0) (= min MIN) (= max MAX) (= containsv 0)) (inv1 i N len containsv min max)))
    ic_antecedent = And(N > 0, len == 0, i == 0, min == MIN, max == MAX, containsv == 0)
    ic_consequent = inv1(i, N, len, containsv, min, max)
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
    print("Checking for first loop inductiveness")
    print("="*40)
    # CHC Rule: (=> (and (inv1...) (< i N) (= v i) (insert...) (= i1 (+ i 1))) (inv1...))
    ic_antecedent = And(inv1(i, N, len, containsv, min, max), is_valid(containsv), i < N,
                        v == i,
                        insert(v, len, containsv, min, max, len1, containsv1, min1, max1),
                        i1 == i + 1)
    ic_consequent = inv1(i1, N, len1, containsv1, min1, max1)
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

def chk_val_transition_1_to_2():
    global chckval
    print("="*51)
    print("Checking transition from first loop to second loop")
    print("="*51)
    # CHC Rule: (=> (and (inv1...) (not (< i N)) (= i1 0)) (inv2...))
    ic_antecedent = And(inv1(i, N, len, containsv, min, max), is_valid(containsv), Not(i < N), i1 == 0)
    ic_consequent = inv2(i1, N, len, containsv, min, max)
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
    print("="*41)
    print("Checking for second loop inductiveness")
    print("="*41)
    # CHC Rule: (=> (and (inv2...) (< i N) (= v i) (erase...) (= i1 (+ i 1))) (inv2...))
    ic_antecedent = And(inv2(i, N, len, containsv, min, max), is_valid(containsv), i < N,
                        v == i,
                        erase(v, len, containsv, min, max, len1, containsv1, min1, max1),
                        i1 == i + 1)
    ic_consequent = inv2(i1, N, len1, containsv1, min1, max1)
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

def chk_val_transition_2_to_3():
    global chckval
    print("="*51)
    print("Checking transition from second loop to third loop")
    print("="*51)
    # CHC Rule: (=> (and (inv2...) (not (< i N)) (reserve...) (= i1 0)) (inv3...))
    ic_antecedent = And(inv2(i, N, len, containsv, min, max), is_valid(containsv), Not(i < N),
                        reserve(len, N, len1),
                        i1 == 0)
    ic_consequent = inv3(i1, N, len, containsv, min, max) # Note: len is passed, not len1
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

def chk_val_invariant3():
    global chckval
    print("="*40)
    print("Checking for third loop inductiveness")
    print("="*40)
    # CHC Rule: (=> (and (inv3...) (< i N) (= v (+ i N)) (insert...) (= i1 (+ i 1))) (inv3...))
    ic_antecedent = And(inv3(i, N, len, containsv, min, max), is_valid(containsv), i < N,
                        v == i + N,
                        insert(v, len, containsv, min, max, len1, containsv1, min1, max1),
                        i1 == i + 1)
    ic_consequent = inv3(i1, N, len1, containsv1, min1, max1)
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
    # CHC Rule: (=> (and (inv3...) (not (< i N)) (not (= len N))) fail))
    correct_condition = (len == N)
    ic_antecedent = And(inv3(i, N, len, containsv, min, max), is_valid(containsv), Not(i < N),
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
        print("Implication is valid (Property holds)")
    s.pop()

# --- Run all checks ---
chk_val_initial_conditions1()
chk_val_invariant1()
chk_val_transition_1_to_2()
chk_val_invariant2()
chk_val_transition_2_to_3()
chk_val_invariant3()
chk_post()

# --- Final result ---
if chckval == 1:
    print("\nqwertyasdfg")