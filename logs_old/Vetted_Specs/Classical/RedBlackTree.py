# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
def inv1(i, N, max, min, len, noDup):
    is_noDup = (noDup == 1)
    
    empty_state = And(len == 0, is_noDup, max < min)
    
    non_empty_state = And(len == i, is_noDup, min == 0, max == i - 1)
    
    return And(i >= 0, i <= N,
               If(i == 0,
                  empty_state,
                  non_empty_state))

def insert(i, max, min, len, noDup, max1, min1, len1, noDup1):
    len_update = (len1 == len + 1)
    
    empty_case = And(max1 == i,
                     min1 == i,
                     noDup1 == noDup)
    
    max_update = (max1 == If(i > max, i, max))
    min_update = (min1 == If(i < min, i, min))
    
    is_dup_possible = And(noDup == 1, len > 0, i >= min, i <= max)
    noDup_update = (noDup1 == If(is_dup_possible, 0, noDup))
    
    non_empty_case = And(max_update, min_update, noDup_update)
    
    return And(len_update,
               If(len == 0,
                  empty_case,
                  non_empty_case))

def search(data, min, max, len, ret1):
    in_range = And(data >= min, data <= max)
    
    is_contiguous = (max - min + 1 == len)
    
    must_succeed = And(len > 0, is_contiguous, in_range)
    
    must_fail = Or(len == 0, Not(in_range))
    
    return And(
        Implies(must_succeed, ret1 == 1),
        Implies(must_fail, ret1 == 0)
    )