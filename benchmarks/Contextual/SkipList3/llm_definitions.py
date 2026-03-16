# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
from z3 import *

def inv1(i, N, isPresent, min, max, len):
    """
    Loop invariant for the main while loop.
    - i: loop counter
    - N: total number of iterations
    - isPresent: flag indicating if at least one element has been inserted
    - min: minimum value seen so far
    - max: maximum value seen so far
    - len: number of elements inserted
    """
    MAX = 128
    MIN = -129

    # Properties that hold true throughout the loop's execution.
    base_properties = And(i == len, i >= 0, i <= N, N > 0)

    # The state of the system can be one of two kinds:
    # 1. The initial state, before any insertions. This only happens when i is 0.
    state_is_initial = And(
        i == 0,
        isPresent == 0,
        min == MAX,
        max == MIN
    )

    # 2. The running state, after at least one insertion. This happens for all i > 0.
    state_is_running = And(
        i > 0,
        isPresent == 1,
        min <= max
    )
    
    # The invariant is that the base properties are always true, and the system
    # is either in its initial state or its running state.
    return And(base_properties, Or(state_is_initial, state_is_running))

def insert(v, isPresent, min, max, len, isPresent1, min1, max1, len1):
    """
    Models the insert operation, updating min, max, len, and isPresent.
    - v: new value being inserted
    - isPresent, min, max, len: current state
    - isPresent1, min1, max1, len1: next state
    """
    # After any insert, the length increments and the 'isPresent' flag is set.
    common_updates = And(
        isPresent1 == 1,
        len1 == len + 1
    )

    # The logic for updating min and max depends on whether this is the first element.
    # The 'isPresent' flag from the pre-state tells us this.
    min_max_updates = If(
        isPresent == 0,
        # Case 1: First element. min and max are both set to the new value.
        And(min1 == v, max1 == v),
        # Case 2: Subsequent element. Update min and max accordingly.
        And(
            min1 == If(v < min, v, min),
            max1 == If(v > max, v, max)
        )
    )

    return And(common_updates, min_max_updates)

def lower_bound(k, lb_ret1):
    """
    Defines the property of the lower_bound function.
    To satisfy the final assertion (assert(lb_ret1 >= min)), this function must
    return a value greater than or equal to its input.
    - k: input value (which will be 'min' from the loop's final state)
    - lb_ret1: return value of the function
    """
    return lb_ret1 >= k