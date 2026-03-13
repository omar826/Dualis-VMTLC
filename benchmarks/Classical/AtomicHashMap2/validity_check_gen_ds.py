from z3 import *

"""
checker for:
(declare-var N Int)
(declare-var len Int)
(declare-var len1 Int)
(declare-var i Int)
(declare-var i1 Int)
(declare-var min Int)
(declare-var min1 Int)
(declare-var max Int)
(declare-var max1 Int)
(declare-var kveq Int)
(declare-var kveq1 Int)
(declare-var kveq2 Int)
(declare-var k Int)
(declare-var v Int)
(declare-var ret1 Int)
(declare-rel insert (Int Int Int Int Int Int Int Int Int Int))
(declare-rel find (Int Int Int Int Int Int))
(declare-rel inv1 (Int Int Int Int Int Int))
(declare-rel inv2 (Int Int Int Int Int Int))
(declare-rel fail ())
(define-fun MAX () Int 128)
(define-fun MIN () Int -129)
(define-fun is_valid ((x Int)) Bool (or (= x 1) (= x 0)))


(rule (=> (and (> N 3) (= len 0) (= i 0) (= min MAX) (= max MIN) (= kveq 1)) (inv1 i N len min max kveq)))

(rule (=> (and (inv1 i N len min max kveq) (is_valid kveq) (< i N) (= k i) (= v i) (insert k v len min max kveq len1 min1 max1 kveq1) (= i1 (+ i 1))) (inv1 i1 N len1 min1 max1 kveq1)))

(rule (=> (and (inv1 i N len min max kveq) (is_valid kveq) (not (< i N)) (= i1 0)) (inv2 i1 N len min max kveq)))

(rule (=> (and (inv2 i N len min max kveq) (is_valid kveq) (< i N) (= k i) (= v i) (insert k v len min max kveq len1 min1 max1 kveq1) (= i1 (+ i 1))) (inv2 i1 N len1 min1 max1 kveq1)))

(rule (=> (and (inv2 i N len min max kveq) (is_valid kveq) (not (< i N)) (not (= k max)) (not (= k min)) (<= 0 k) (< k N) (find k len min max kveq ret1) (not (= ret1 k))) fail))

(query fail :print-certificate true)


"""
# Define variables from CHC
N = Int('N')
len_var = Int('len')
len1 = Int('len1')
i = Int('i')
i1 = Int('i1')
min_var = Int('min')
min1 = Int('min1')
max_var = Int('max')
max1 = Int('max1')
k = Int('k')
v = Int('v')
ret1 = Int('ret1')
kveq = Int('kveq')
kveq1 = Int('kveq1')


# Define constants from CHC
MAX = 128
MIN = -129

# Global flag to track if all checks pass
chckval = 1

try:
    from llm_definitions import inv1, inv2, insert, find
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
    # CHC Rule: (=> (and (> N 3) (= len 0) (= i 0) (= min MAX) (= max MIN) (= kveq 1)) (inv1...))
    ic_antecedent = And(N > 3, len_var == 0, i == 0, min_var == MAX, max_var == MIN, kveq == 1)
    ic_consequent = inv1(i, N, len_var, min_var, max_var, kveq)
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
    # CHC Rule: (=> (and (inv1...) (< i N) (insert...) (= i1 (+ i 1))) (inv1...))
    ic_antecedent = And(inv1(i, N, len_var, min_var, max_var, kveq), is_valid(kveq), i < N,
                        k == i, v == i,
                        insert(k, v, len_var, min_var, max_var, kveq, len1, min1, max1, kveq1),
                        i1 == i + 1)
    ic_consequent = inv1(i1, N, len1, min1, max1, kveq1)
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

def chk_val_transition():
    global chckval
    print("="*51)
    print("Checking transition from first loop to second loop")
    print("="*51)
    # CHC Rule: (=> (and (inv1...) (not (< i N)) (= i1 0)) (inv2...))
    ic_antecedent = And(inv1(i, N, len_var, min_var, max_var, kveq), is_valid(kveq), Not(i < N), i1 == 0)
    ic_consequent = inv2(i1, N, len_var, min_var, max_var, kveq)
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
    # CHC Rule: (=> (and (inv2...) (< i N) (insert...) (= i1 (+ i 1))) (inv2...))
    ic_antecedent = And(inv2(i, N, len_var, min_var, max_var, kveq), is_valid(kveq), i < N,
                        k == i, v == i,
                        insert(k, v, len_var, min_var, max_var, kveq, len1, min1, max1, kveq1),
                        i1 == i + 1)
    ic_consequent = inv2(i1, N, len1, min1, max1, kveq1)
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
    # CHC Rule: (=> (and (inv2...) (not (< i N)) (not (= k max)) (not (= k min)) (<= 0 k) (< k N) (find...) (not (= ret1 k))) fail)
    ic_antecedent = And(inv2(i, N, len_var, min_var, max_var, kveq), is_valid(kveq), Not(i < N),
                        Not(k == max_var), Not(k == min_var), 0 <= k, k < N,
                        find(k, len_var, min_var, max_var, kveq, ret1),
                        Not(ret1 == k))
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
chk_val_transition()
chk_val_invariant2()
chk_post()

# --- Final result ---
if chckval == 1:
    print("\nqwertyasdfg")

