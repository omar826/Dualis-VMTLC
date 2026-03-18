# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
def inv1(i, N, len, min, max, kveq):
    MAX = 128
    MIN = -129
    
    initial_state = And(min == MAX, max == MIN)
    loop_state = And(min == 0, max == i - 1)
    
    return And(i >= 0, i <= N,
               N > 0,
               kveq == 1,
               len == i,
               If(i == 0, initial_state, loop_state))

def inv2(i, N, len, min, max, kveq):
    return And(i >= 0, i <= N,
               N > 0,
               kveq == 1,
               len == N,
               min == 0,
               max == N - 1)

def insert(k, v, len, min, max, kveq, len1, min1, max1, kveq1):
    min1_def = If(k < min, k, min)
    max1_def = If(k > max, k, max)
    
    kveq1_def = If(And(kveq == 1, k == v), 1, 0)
    
    is_new = Or(len == 0, k < min, k > max)
    len1_def = If(is_new, len + 1, len)
    
    return And(len1 == len1_def,
               min1 == min1_def,
               max1 == max1_def,
               kveq1 == kveq1_def)

def find(k, len, min, max, kveq, ret1):
    MAX = 128
    
    # A key is guaranteed to be present if the collection state matches the specific
    # properties created by the client: a dense mapping where all keys equal their values.
    # This is abstracted by checking if len matches the size of the [min, max] range
    # and the `kveq` property holds.
    is_dense_kveq_collection = And(len > 0, len == max - min + 1, kveq == 1)
    key_in_range = And(k >= min, k <= max)
    
    must_succeed = And(is_dense_kveq_collection, key_in_range)
    
    # The specification states that if the conditions for guaranteed success are met,
    # then the find operation must not fail (i.e., return MAX).
    # For all other cases (e.g., sparse collections), the function is allowed to
    # either succeed or fail, making the specification more general.
    return Implies(must_succeed, ret1 != MAX)