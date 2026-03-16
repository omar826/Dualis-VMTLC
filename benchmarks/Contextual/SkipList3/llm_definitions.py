# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
from z3 import *

def inv1(i, N, isPresent, min, max, len):
    initial_state = And(i == 0,
                        isPresent == 0,
                        min == 128,
                        max == -129,
                        len == 0)
    
    loop_state = And(i > 0,
                     isPresent == 1,
                     min <= max,
                     len == i)

    return And(i >= 0, i <= N, Or(initial_state, loop_state))

def insert(v, isPresent, min, max, len, isPresent1, min1, max1, len1):
    is_first_insert = (len == 0)
    
    min_update = If(is_first_insert, v, If(v < min, v, min))
    max_update = If(is_first_insert, v, If(v > max, v, max))
    
    return And(len1 == len + 1,
               isPresent1 == 1,
               min1 == min_update,
               max1 == max_update)

def lower_bound(k, min, max, lb_ret1):
    return lb_ret1 == k