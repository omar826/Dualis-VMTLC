# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
def inv1(i_old, N, len, min, max, kveq):
    MAX = 128
    MIN = -129
    
    cond_N = (N > 0)
    cond_i = And(i_old >= 0, i_old <= N)
    cond_len = (len == i_old)
    cond_kveq = (kveq == 1)
    
    initial_state = And(min == MAX, max == MIN)
    loop_state = And(min == 0, max == i_old - 1)
    
    cond_min_max = If(i_old == 0, initial_state, loop_state)
    
    return And(cond_N, cond_i, cond_len, cond_kveq, cond_min_max)

def inv2(i, N, len, min, max, kveq):
    cond_N = (N > 0)
    cond_i = And(i >= 0, i <= N)
    cond_len = (len == N)
    cond_min = (min == 0)
    cond_max = (max == N - 1)
    cond_kveq = (kveq == 1)
    
    return And(cond_N, cond_i, cond_len, cond_min, cond_max, cond_kveq)

def insert(k, v, len, min, max, kveq, len1, min1, max1, kveq1):
    is_dense = If(len > 0, len == max - min + 1, True)
    is_outside_bounds = Or(k < min, k > max)

    S_inserted = And(len1 == len + 1,
                     min1 == If(k < min, k, min),
                     max1 == If(k > max, k, max),
                     kveq1 == If(And(kveq == 1, k == v), 1, 0))

    S_no_change = And(len1 == len,
                      min1 == min,
                      max1 == max,
                      kveq1 == kveq)

    return If(is_outside_bounds,
              S_inserted,
              If(is_dense,
                 S_no_change,
                 Or(S_no_change, S_inserted)))

def find(k, len, min, max, kveq, ret1):
    MAX = 128
    
    is_dense = If(len > 0, len == max - min + 1, True)
    is_within_bounds = And(k >= min, k <= max)
    
    must_succeed = And(len > 0, is_dense, is_within_bounds)
    must_fail = Or(len == 0, Not(is_within_bounds))
    
    success = If(kveq == 1, ret1 == k, ret1 != MAX)
    failure = (ret1 == MAX)
    
    return If(must_succeed,
              success,
              If(must_fail,
                 failure,
                 Or(success, failure)))