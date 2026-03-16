# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
def inv1(i, N, isPresent, min, max, len):
    i_range_cond = And(i >= 0, i <= N)
    len_cond = (len == i)
    min_max_cond = If(i == 0,
                      And(min == 128, max == -129),
                      And(min == 0, max == i - 1))
    return And(i_range_cond, len_cond, min_max_cond)

def insert(v, isPresent, min, max, len, isPresent1, min1, max1, len1):
    len_update = (len1 == len + 1)
    min_update = (min1 == If(len == 0, v, If(v < min, v, min)))
    max_update = (max1 == If(len == 0, v, If(v > max, v, max)))
    is_present_update = (isPresent1 == 1)
    return And(len_update, min_update, max_update, is_present_update)

def lower_bound(k, min, max, lb_ret1):
    return (lb_ret1 == k)