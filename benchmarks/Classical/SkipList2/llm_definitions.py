# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
def inv1(i, N, isPresent, min, max, len):
    initial_state = And(isPresent == 0, min == 128, max == -129)
    loop_state = And(isPresent == 1, min == 0, max == i - 1)
    return And(
        i >= 0,
        i <= N,
        len == i,
        If(i == 0, initial_state, loop_state)
    )

def insert(v, isPresent, min, max, len, isPresent1, min1, max1, len1):
    post_len = len + 1
    post_min = If(len == 0, v, If(v < min, v, min))
    post_max = If(len == 0, v, If(v > max, v, max))
    post_isPresent = 1
    return And(
        len1 == post_len,
        min1 == post_min,
        max1 == post_max,
        isPresent1 == post_isPresent
    )

def lower_bound(k, lb_ret1):
    return lb_ret1 >= k