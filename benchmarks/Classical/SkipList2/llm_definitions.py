# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
def inv1(i, N, isPresent, min, max, len):
    MAX = 128
    MIN = -129
    cond_i_range = And(i >= 0, i <= N)
    cond_len = (len == i)
    empty_state = And(min == MAX, max == MIN)
    non_empty_state = And(min == 0, max == i - 1)
    cond_min_max = If(i == 0, empty_state, non_empty_state)
    return And(cond_i_range, cond_len, cond_min_max)

def insert(v, isPresent, min, max, len, isPresent1, min1, max1, len1):
    add_element_logic = And(
        len1 == len + 1,
        If(len == 0,
           And(min1 == v, max1 == v),
           And(min1 == If(v < min, v, min),
               max1 == If(v > max, v, max))
        )
    )
    return And(add_element_logic, isPresent1 == 1)

def lower_bound(k, min, max, lb_ret1):
    return Implies(And(min <= max, k <= max), lb_ret1 >= k)