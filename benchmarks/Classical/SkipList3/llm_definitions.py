# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
def inv1(i, N, isPresent, min, max, len):
    i_and_len_relation = And(i >= 0, i <= N, i == len)

    state_properties = If(
        len == 0,
        And(isPresent == 0, min == 128, max == -129),
        And(isPresent == 1, min <= max)
    )

    return And(i_and_len_relation, state_properties)

def insert(v, isPresent, min, max, len, isPresent1, min1, max1, len1):
    len_update = (len1 == len + 1)
    min_update = (min1 == If(v < min, v, min))
    max_update = (max1 == If(v > max, v, max))
    present_update = (isPresent1 == 1)

    return And(len_update, min_update, max_update, present_update)

def lower_bound(k, lb_ret1):
    return lb_ret1 >= k