# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
def inv1(i, N, len, min, max):
    return And(i >= 0, i <= N,
               len == i,
               If(i == 0,
                  And(min == 128, max == -129),
                  And(min == 0, max == i - 1)))

def insert(k, v, len, min, max, len1, min1, max1):
    is_new_key = Or(len == 0, k < min, k > max)
    
    add_spec = And(
        len1 == len + 1,
        min1 == If(len == 0, k, If(k < min, k, min)),
        max1 == If(len == 0, k, If(k > max, k, max))
    )
    
    update_spec = And(
        len1 == len,
        min1 == min,
        max1 == max
    )
    
    return If(is_new_key, add_spec, update_spec)

def find(k, len, min, max, ret1):
    is_present = And(len > 0, k >= min, k <= max)
    return If(is_present, ret1 != -129, ret1 == -129)