# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
def insert(k, v, len, min, max, kveq, len1, min1, max1, kveq1):
    is_present = And(0 <= k, k < len)
    return And(
        len1 == If(is_present, len, len + 1),
        min1 == If(is_present, min, If(k < min, k, min)),
        max1 == If(is_present, max, If(k > max, k, max)),
        kveq1 == If(is_present, kveq, If(And(kveq == 1, k == v), 1, 0))
    )

def inv1(i, N, len, min, max, kveq):
    MAX = 128
    MIN = -129
    return And(
        i >= 0,
        i <= N,
        len == i,
        If(i == 0,
           And(min == MAX, max == MIN),
           And(min == 0, max == i - 1))
    )

def inv2(i, N, len, min, max, kveq):
    MAX = 128
    MIN = -129
    return And(
        i >= 0,
        i <= N,
        len == N,
        min == If(N == 0, MAX, 0),
        max == If(N == 0, MIN, N - 1)
    )