# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
def inv1(i, N, isPresent, min, max, len):
    i_invariant = And(i >= 0, i <= N)
    
    # At i=0, the collection is in its initial state where min is greater than max.
    # The invariant must hold for any initial `len` or `isPresent`, as they are not
    # constrained in the first CHC rule's antecedent.
    initial_state = And(i == 0, min > max)

    # For i > 0, at least one element has been inserted. This means `min <= max`
    # must hold. Also, the `insert` function guarantees that `isPresent` will be 1.
    loop_state = And(i > 0, min <= max, isPresent == 1)
    
    min_max_ispresent_invariant = Or(initial_state, loop_state)

    return And(i_invariant, min_max_ispresent_invariant)

def insert(v, isPresent, min, max, len, isPresent1, min1, max1, len1):
    # The collection is considered empty if min > max.
    is_empty = (min > max)
    
    # If the collection is empty, the new min and max are both 'v'.
    # Otherwise, update min and max by taking the min/max of the current values and 'v'.
    new_min = If(is_empty, v, If(v < min, v, min))
    new_max = If(is_empty, v, If(v > max, v, max))
    
    # Post-conditions of the insert operation.
    return And(
        # After an insert, the collection is not empty, so isPresent becomes 1.
        isPresent1 == 1,
        # The length is incremented by 1.
        len1 == len + 1,
        # The min and max values are updated according to the logic above.
        min1 == new_min,
        max1 == new_max
    )

def lower_bound(k, min, max, lb_ret1):
    # The client program calls this function with k=max and asserts that the
    # return value is also max. The simplest specification that is general
    # and strong enough to prove this assertion is that the function returns its input key 'k'.
    return (lb_ret1 == k)