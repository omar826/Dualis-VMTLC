# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
def inv1(i, N, len, min, max, kveq):
    MAX = 128
    MIN = -129
    return And(N > 0,
               i >= 0,
               i <= N,
               len == i,
               Or(And(i == 0, min == MAX, max == MIN),
                  And(i > 0, min == 0, max == i - 1)))

def inv2(i, N, len, min, max, kveq):
    return And(N > 0,
               i >= 0,
               i <= N,
               len == N,
               min == 0,
               max == N - 1)

def insert(k, v, len, min, max, kveq, len1, min1, max1, kveq1):
    is_empty = (len == 0)
    
    transition_add = And(
        len1 == len + 1,
        min1 == If(is_empty, k, If(k < min, k, min)),
        max1 == If(is_empty, k, If(k > max, k, max)),
        kveq1 == If(And(kveq == 1, k == v), 1, 0)
    )
    
    transition_noop = And(
        len1 == len,
        min1 == min,
        max1 == max,
        kveq1 == kveq
    )
    
    must_add = Or(is_empty, k < min, k > max)
    
    is_dense = And(len > 0, len == max - min + 1)
    key_in_range = And(k >= min, k <= max)
    must_be_duplicate = And(is_dense, key_in_range)
    
    return If(
        must_add,
        transition_add,
        If(
            must_be_duplicate,
            transition_noop,
            Or(transition_add, transition_noop)
        )
    )