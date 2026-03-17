# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
def inv1(i, N, isPresent, min, max, len):
    initial_state_props = And(i == 0,
                              min == 128,
                              max == -129)
    loop_state_props = And(i > 0,
                           isPresent == 1,
                           len == 1,
                           min == 1,
                           max == 1)
    return And(N > 0, i >= 0, i <= N, Or(initial_state_props, loop_state_props))

def insert(v, isPresent, min, max, len, isPresent1, min1, max1, len1):
    precondition = Implies(And(min == 128, max == -129), And(len == 0, isPresent == 0))
    
    # Behavior when value is already present (or collection is considered full by this logic)
    # Note: isPresent flag means "something is present", not necessarily v
    was_present_behavior = And(isPresent1 == 1, min1 == min, max1 == max, len1 == len)

    # Behavior when inserting a new value
    is_empty_collection = And(len == 0, isPresent == 0) # Derived from client logic
    update_min = If(is_empty_collection, v, If(v < min, v, min))
    update_max = If(is_empty_collection, v, If(v > max, v, max))
    not_present_behavior = And(isPresent1 == 1, len1 == len + 1, min1 == update_min, max1 == update_max)

    postcondition = If(isPresent == 1, was_present_behavior, not_present_behavior)

    return And(precondition, postcondition)