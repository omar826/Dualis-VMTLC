# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
def inv1(i, N, isPresent, min, max, len):
    initial_state = And(
        len == 0,
        min == 128,
        max == -129,
        isPresent == 0
    )
    
    loop_state = And(
        len == i,
        min == 0,
        max == i - 1,
        isPresent == 1
    )
    
    return And(
        i >= 0,
        i <= N,
        If(i == 0, initial_state, loop_state)
    )

def insert(v, isPresent, min, max, len, isPresent1, min1, max1, len1):
    new_min = If(len == 0, v, If(v < min, v, min))
    
    new_max = If(len == 0, v, If(v > max, v, max))
    
    return And(
        len1 == len + 1,
        min1 == new_min,
        max1 == new_max,
        isPresent1 == 1
    )

def remove(k, min, max, len, min1, max1, len1, ret1):
    precondition_for_guaranteed_success = And(
        len > 0,
        len == max - min + 1,
        k >= min,
        k <= max
    )
    
    guaranteed_behavior = Implies(
        precondition_for_guaranteed_success,
        len1 == len - 1
    )
    
    possible_outcomes = Or(
        len1 == len - 1,
        len1 == len
    )
    
    return_value_spec = And(
        Implies(len1 == len - 1, ret1 == 1),
        Implies(len1 == len, ret1 == 0)
    )

    return And(guaranteed_behavior, possible_outcomes, return_value_spec)