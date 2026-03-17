# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
def inv1(i, N, len, min, max, kveq):
    MAX = 128
    MIN = -129
    is_empty = And(min == MAX, max == MIN)
    is_not_empty = And(min == 0, max == i - 1)
    return And(
        N > 0,
        i >= 0,
        i <= N,
        len == i,
        kveq == 1,
        If(i == 0, is_empty, is_not_empty)
    )

def inv2(i, N, len, min, max, kveq):
    return And(
        N > 0,
        i >= 0,
        i <= N,
        len == N + i,
        kveq == 1,
        min == 0,
        max == N - 1
    )

def insert(k, v, len, min, max, kveq, len1, min1, max1, kveq1):
    MAX = 128
    MIN = -129
    cond_len = (len1 == len + 1)
    cond_min = (min1 == If(len == 0, k, If(k < min, k, min)))
    cond_max = (max1 == If(len == 0, k, If(k > max, k, max)))
    cond_kveq = (kveq1 == If(k == v, kveq, 0))
    
    return And(cond_len, cond_min, cond_max, cond_kveq)

def find(k, len, min, max, kveq, ret1):
    MAX = 128
    can_be_found = And(len > 0, k >= min, k <= max)
    
    return If(can_be_found, ret1 != MAX, ret1 == MAX)