# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
def inv1(i, N, isPresent, min, max, len):
    MAX = 128
    MIN = -129
    is_initial_state = And(i == 0, len == 0, isPresent == 0, min == MAX, max == MIN)
    is_loop_state = And(i > 0, len == i, isPresent == 1, min == 1, max == 1)
    return And(i >= 0, i <= N, Or(is_initial_state, is_loop_state))

def insert(v, isPresent, min, max, len, isPresent1, min1, max1, len1):
    new_min = If(len == 0, v, If(v < min, v, min))
    new_max = If(len == 0, v, If(v > max, v, max))
    return And(isPresent1 == 1,
               min1 == new_min,
               max1 == new_max,
               len1 == len + 1)

def lower_bound(k, min, max, lb_ret1):
    return And(lb_ret1 >= k, Implies(k <= min, lb_ret1 == min))