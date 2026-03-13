from z3 import *

# Define variables from CHC
b_size = Int('b_size')
c_rate = Int('c_rate')
avai_tokens = Int('avai_tokens')
avai_tokens1 = Int('avai_tokens1')
consumed_tokens = Int('consumed_tokens')
consumed_tokens1 = Int('consumed_tokens1')
token_counter = Int('token_counter')

# Global flag to track if all checks pass
chckval = 1

try:
    from llm_definitions import inv1, generateTokens, consume
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
    # CHC Rule: (=> (and (> b_size 0) (> c_rate 0) (>= b_size c_rate) (= consumed_tokens1 0) (generateTokens b_size avai_tokens1)) (inv1 avai_tokens1 b_size c_rate consumed_tokens1))
    ic_antecedent = And(b_size > 0, c_rate > 0, b_size >= c_rate,
                        consumed_tokens1 == 0,
                        generateTokens(b_size, avai_tokens1))
    ic_consequent = inv1(avai_tokens1, b_size, c_rate, consumed_tokens1)
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
    print("="*36)
    print("Checking for loop inductiveness")
    print("="*36)
    # CHC Rule: (=> (and (inv1 avai_tokens b_size c_rate consumed_tokens) (>= avai_tokens c_rate) (consume c_rate avai_tokens avai_tokens1) (= consumed_tokens1 (+ consumed_tokens c_rate))) (inv1 avai_tokens1 b_size c_rate consumed_tokens1))
    ic_antecedent = And(inv1(avai_tokens, b_size, c_rate, consumed_tokens),
                        avai_tokens >= c_rate,
                        consume(c_rate, avai_tokens, avai_tokens1),
                        consumed_tokens1 == consumed_tokens + c_rate)
    ic_consequent = inv1(avai_tokens1, b_size, c_rate, consumed_tokens1)
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
    # CHC Rule: (=> (and (inv1 avai_tokens b_size c_rate consumed_tokens) (not (>= avai_tokens c_rate)) (not (<= consumed_tokens b_size) )) fail))
    correct_condition = (consumed_tokens <= b_size)
    ic_antecedent = And(inv1(avai_tokens, b_size, c_rate, consumed_tokens),
                        Not(avai_tokens >= c_rate),
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
chk_val_invariant1()
chk_post()

# --- Final result ---
if chckval == 1:
    print("\nqwertyasdfg")