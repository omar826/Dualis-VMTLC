# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
def insert(k, v, len, min, max, kveq, len1, min1, max1, kveq1):
    is_present = And(len > 0, k >= min, k <= max)
    
    add_behavior = And(
        len1 == len + 1,
        min1 == If(k < min, k, min),
        max1 == If(k > max, k, max),
        kveq1 == If(And(kveq == 1, k == v), 1, 0)
    )
    
    noop_behavior = And(
        len1 == len,
        min1 == min,
        max1 == max,
        kveq1 == kveq
    )
    
    return Or(
        And(Not(is_present), add_behavior),
        And(is_present, Or(add_behavior, noop_behavior))
    )

def find(k, len, min, max, kveq, ret1):
    return Implies(And(len > 0, k == max, kveq == 1), ret1 != 128)

def inv1(i, N, len, min, max, kveq):
    i_range = And(i >= 0, i <= N)
    len_prop = (len == i)
    kveq_prop = (kveq == 1)
    min_max_prop = If(i == 0,
                      And(min == 128, max == -129),
                      And(min == 0, max == i - 1))
    return And(N > 0, i_range, len_prop, kveq_prop, min_max_prop)

def inv2(i, N, len, min, max, kveq):
    i_range = And(i >= 0, i <= N)
    len_prop = And(len >= N, len <= N + i)
    min_prop = (min == 0)
    max_prop = (max == N - 1)
    kveq_prop = (kveq == 1)
    return And(N > 0, i_range, len_prop, min_prop, max_prop, kveq_prop)