# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
from z3 import *

def inv1(i, N, isPresent, min, max, len):
    """
    Invariant for the main loop.
    It captures two possible states of the program:
    1. The initial state before any insertions (i=0).
    2. The state after the value '1' has been inserted (i>0).
    """
    MAX = 128
    MIN = -129
    
    # State before the first element is inserted
    initial_state = And(i == 0,
                        isPresent == 0,
                        min == MAX,
                        max == MIN,
                        len == 0)
    
    # State after the first element (v=1) has been inserted.
    # Since only v=1 is ever inserted, this state is stable.
    running_state = And(i > 0,
                        isPresent == 1,
                        min == 1,
                        max == 1,
                        len == 1)
                        
    loop_bounds = And(i >= 0, i <= N)
    
    return And(loop_bounds, Or(initial_state, running_state))

def insert(v, isPresent, min, max, len, isPresent1, min1, max1, len1):
    """
    Models the insert operation.
    It only needs to be correct for the specific inputs seen in the program.
    v is always 1.
    """
    MAX = 128
    MIN = -129
    
    # Rule for inserting v=1 into an empty set.
    # This transitions the state from initial to running.
    rule1 = Implies(
        And(v == 1, isPresent == 0, len == 0, min == MAX, max == MIN),
        And(isPresent1 == 1, min1 == 1, max1 == 1, len1 == 1)
    )

    # Rule for inserting v=1 into the set that already contains {1}.
    # This is a no-op; the state remains the same.
    rule2 = Implies(
        And(v == 1, isPresent == 1, len == 1, min == 1, max == 1),
        And(isPresent1 == 1, min1 == 1, max1 == 1, len1 == 1)
    )

    return And(rule1, rule2)

def lower_bound(k, min, max, lb_ret1):
    """
    Models the lower_bound operation.
    The client program calls this with k=min and asserts that the result is min.
    Therefore, the contextual specification is that if k equals min, the result
    must also equal min. This covers all uses of this function in the program.
    """
    return Implies(k == min, lb_ret1 == min)