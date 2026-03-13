# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
def inv1(i, N, len, min, max):
    loop_counter_bound = And(i >= 0, i <= N)
    len_is_correct = (len == i)
    min_max_is_correct = If(i == 0,
                            And(min == 128, max == -129),
                            And(min == 0, max == i - 1))
                            
    return And(loop_counter_bound, len_is_correct, min_max_is_correct)

def insert(k, v, len, min, max, len1, min1, max1):
    is_empty_before = (len == 0)
    
    is_new = Not(And(k >= min, k <= max))
    
    spec_len = If(is_empty_before,
                  len1 == 1,
                  If(is_new, len1 == len + 1, len1 == len))

    spec_min = If(is_empty_before,
                  min1 == k,
                  min1 == If(k < min, k, min))

    spec_max = If(is_empty_before,
                  max1 == k,
                  max1 == If(k > max, k, max))

    return And(spec_len, spec_min, spec_max)

def find(k, len, min, max, ret1):
    key_is_in_range = And(k >= min, k <= max)
    
    return If(key_is_in_range, ret1 != -129, ret1 == -129)