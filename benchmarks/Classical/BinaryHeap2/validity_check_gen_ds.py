from z3 import *

# Define variables from CHC
N = Int('N')
i = Int('i')
i1 = Int('i1')
isHeap = Int('isHeap')
isHeap1 = Int('isHeap1')
isHeap2 = Int('isHeap2')
len = Int('len')
len1 = Int('len1')
ret1 = Int('ret1')

chckval = 1  # Used to track if all checks pass

try:
    from llm_definitions import inv1, insert, deleteMin, downHeap
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

def chk_val_initial_conditions():
    global chckval
    print("="*48)
    print("Checking if initial conditions imply loop invariant")
    print("="*48)
    # CHC Rule: (=> (and (> N 0) (= i1 0) (= isHeap1 1) (= len1 0)) (inv1 i1 N isHeap1 len1))
    ic_antecedent = And(N > 0, i1 == 0, isHeap1 == 1, len1 == 0)
    ic_consequent = inv1(i1, N, isHeap1, len1)
    ic_implication = Implies(ic_antecedent, ic_consequent)

    s.push()
    print("\nAntecedent:", ic_antecedent)
    s.add(ic_antecedent)
    print("Checking if antecedent is satisfiable:")
    if s.check() == sat:
        print("Antecedent is satisfiable")
        print("Model:", s.model())
    else:
        print("Antecedent is always false")
    s.pop()

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
    print("="*36)
    print("Checking for loop inductiveness")
    print("="*36)
    # CHC Rule: (=> (and (inv1 i N isHeap len ) (is_valid isHeap) (< i N) (insert i isHeap len  isHeap1 len1) (= i1 (+ i 1))) (inv1 i1 N isHeap1 len1 )))
    ic_antecedent = And(inv1(i, N, isHeap, len),
                        is_valid(isHeap),
                        i < N,
                        insert(i, isHeap, len, isHeap1, len1),
                        i1 == i + 1)
    ic_consequent = inv1(i1, N, isHeap1, len1)
    ic_implication = Implies(ic_antecedent, ic_consequent)

    s.push()
    print("\nAntecedent:", ic_antecedent)
    s.add(ic_antecedent)
    print("Checking if antecedent is satisfiable:")
    if s.check() == sat:
        print("Antecedent is satisfiable")
        print("Model:", s.model())
    else:
        print("Antecedent is always false")
    s.pop()

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
    # CHC Rule: (=> (and (inv1 i N isHeap len) (is_valid isHeap) (not (< i N)) (deleteMin len isHeap len1 ret1 isHeap1) (is_valid isHeap1) (downheap isHeap2) (is_valid isHeap2) (not (= isHeap2 1))) fail))
    correct_condition = (isHeap2 == 1)
    ic_antecedent = And(inv1(i, N, isHeap, len),
                        is_valid(isHeap),
                        Not(i < N),
                        deleteMin(len, isHeap, len1, ret1, isHeap1),
                        is_valid(isHeap1),
                        downHeap(isHeap2),
                        is_valid(isHeap2),
                        Not(correct_condition))
    ic_consequent = fail()
    ic_implication = Implies(ic_antecedent, ic_consequent)

    s.push()
    print("\nAntecedent:", ic_antecedent)
    s.add(ic_antecedent)
    print("Checking if antecedent is satisfiable:")
    if s.check() == sat:
        print("Antecedent is satisfiable (potential violation):")
        print("Model:", s.model())
    else:
        print("Antecedent is not satisfiable (property holds)")
    s.pop()

    s.push()
    print("\nImplication:", ic_implication)
    s.add(Not(ic_implication))
    print("Checking validity of implication:")
    if s.check() == sat:
        print("Counterexample found (Implication is not valid):")
        print("Model:", s.model())
        chckval = 0
    else:
        print("Implication is valid (property holds)")
    s.pop()

chk_val_initial_conditions()
chk_val_invariant1()
chk_post()

if chckval == 1:
    print("qwertyasdfg")