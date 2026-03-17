# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
from z3 import *

# Helper constants defined in the CHC
MAX = 128
MIN = -129

def inv1(i, N, isPresent, min, max, len):
    """
    Defines the loop invariant.
    - N > 0: This is a precondition from the program that must hold throughout. It's necessary to prove the post-condition.
    - i is bounded by 0 and N.
    - If i == 0 (before the loop starts): The invariant only constrains min and max. This is because the initial CHC rule
      does not provide values for 'len' and 'isPresent', so a stronger invariant would fail the validity check.
    - If i > 0 (inside the loop): The state is fully determined, as the program always inserts the same value (1).
    """
    # Properties of the state before any insertions.
    # We only constrain variables mentioned in the antecedent of the first CHC rule.
    initial_props = And(min == MAX, max == MIN)

    # Properties of the state after one or more insertions.
    loop_props = And(isPresent == 1, len == 1, min == 1, max == 1)

    return And(
        N > 0,
        i >= 0,
        i <= N,
        If(i == 0, initial_props, loop_props)
    )

def insert(v, isPresent, min, max, len, isPresent1, min1, max1, len1):
    """
    Defines the state transition for the insert operation.
    The invariant for i=0 is too weak to constrain 'len', so we cannot use 'len == 0'
    to detect the first insertion. Instead, we use the unique values of 'min' and 'max'
    from the pre-insertion state, which are constrained by the invariant.
    """
    # The state before any insertion is uniquely identified by min/max values.
    is_first_insertion = And(min == MAX, max == MIN)

    # If it's the first insertion, the state transitions to holding only 'v'.
    insert_into_empty = And(
        isPresent1 == 1,
        len1 == 1,
        min1 == v,
        max1 == v
    )
    
    # In this specific program, any subsequent insertion is a duplicate of the value 1,
    # so the state does not change.
    insert_duplicate = And(
        isPresent1 == isPresent,
        len1 == len,
        min1 == min,
        max1 == max
    )
    
    return If(is_first_insertion, insert_into_empty, insert_duplicate)