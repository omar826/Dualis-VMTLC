# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
from z3 import *

MAX = 128
MIN = -129

def inv1(i, N, len, min, max, kveq):
    initial_props = And(len == 0, min == MAX, max == MIN)
    
    loop_props = And(len == i, min == 0, max == i - 1, kveq == 1)
    
    return And(N > 0,
               i >= 0, i <= N,
               If(i == 0, initial_props, loop_props))

def inv2(i, N, len, min, max, kveq):
    return And(N > 0,
               i >= 0, i <= N,
               len == N,
               kveq == 1,
               min == 0,
               max == N - 1)

def insert(k, v, len, min, max, kveq, len1, min1, max1, kveq1):
    update_case = And(
        len1 == len,
        min1 == min,
        max1 == max,
        kveq1 == kveq
    )
    insertion_case = And(
        len1 == len + 1,
        min1 == If(len == 0, k, If(k < min, k, min)),
        max1 == If(len == 0, k, If(k > max, k, max)),
        kveq1 == If(And(k == v, Or(len == 0, kveq == 1)), 1, 0)
    )

    is_out_of_range = Or(k < min, k > max)
    is_contiguous = And(len > 0, max - min + 1 == len)
    is_in_contiguous_range = And(is_contiguous, k >= min, k <= max)

    return If(
        Or(len == 0, is_out_of_range),
        insertion_case,
        If(
            is_in_contiguous_range,
            update_case,
            Or(update_case, insertion_case)
        )
    )