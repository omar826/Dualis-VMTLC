# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
def inv1(i, N, len, min, max, kveq):
    precondition = (N > 3)
    i_is_len = (len == i)
    loop_bounds = And(i >= 0, i <= N)
    min_max_state = If(i == 0,
                       And(min == 128, max == -129),
                       And(min == 0, max == i - 1))
    kveq_state = (kveq == 1)
    return And(precondition, i_is_len, loop_bounds, min_max_state, kveq_state)

def inv2(i, N, len, min, max, kveq):
    precondition = (N > 3)
    loop_bounds = And(i >= 0, i <= N)
    ds_state = And(len == N,
                   min == 0,
                   max == N - 1,
                   kveq == 1)
    return And(precondition, loop_bounds, ds_state)

def insert(k, v, len, min, max, kveq, len1, min1, max1, kveq1):
    len_updates = (len1 == len + 1)
    min_updates = (min1 == If(len == 0, k, If(k < min, k, min)))
    max_updates = (max1 == If(len == 0, k, If(k > max, k, max)))
    kveq_updates = (kveq1 == If(k == v, kveq, 0))
    return And(len_updates, min_updates, max_updates, kveq_updates)

def insert1(k, v, len, min, max, kveq, len1, min1, max1, kveq1):
    return And(len1 == len,
               min1 == min,
               max1 == max,
               kveq1 == kveq)

def find(k, len, min, max, kveq, ret1):
    key_is_present = And(k >= 0, k < len)
    return If(key_is_present,
              ret1 == k,
              Or(ret1 == -129, ret1 == 128))