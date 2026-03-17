# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
def inv1(i, N, len, containsv, min, max):
    MIN = 32767
    MAX = -32768
    is_initial_state = (i == 0)
    initial_cond = And(min == MIN, max == MAX)
    loop_cond = And(min == 0, max == i - 1)
    
    main_properties = And(0 <= i, i <= N, len == i)
    min_max_properties = If(is_initial_state, initial_cond, loop_cond)
    
    return And(main_properties, min_max_properties)

def inv2(i, N, len, containsv, min, max):
    MIN = 32767
    MAX = -32768
    is_final_state = (i == N)
    final_cond = And(min == MIN, max == MAX)
    loop_cond = And(min == i, max == N - 1)

    main_properties = And(0 <= i, i <= N, len == N - i)
    min_max_properties = If(is_final_state, final_cond, loop_cond)
    
    return And(main_properties, min_max_properties)

def inv3(i, N, len, containsv, min, max):
    MIN = 32767
    MAX = -32768
    is_initial_state = (i == 0)
    initial_cond = And(min == MIN, max == MAX)
    loop_cond = And(min == N, max == N + i - 1)
    
    main_properties = And(0 <= i, i <= N, len == i)
    min_max_properties = If(is_initial_state, initial_cond, loop_cond)
    
    return And(main_properties, min_max_properties)

def insert(v, len, containsv, min, max, len1, containsv1, min1, max1):
    len_post = (len1 == len + 1)
    containsv_post = Or(containsv1 == 0, containsv1 == 1)
    
    is_empty = (len == 0)
    
    min_post_if_empty = (min1 == v)
    max_post_if_empty = (max1 == v)
    
    min_post_if_not_empty = (min1 == If(v < min, v, min))
    max_post_if_not_empty = (max1 == If(v > max, v, max))

    min_post = If(is_empty, min_post_if_empty, min_post_if_not_empty)
    max_post = If(is_empty, max_post_if_empty, max_post_if_not_empty)

    return And(len_post, containsv_post, min_post, max_post)

def erase(v, len, containsv, min, max, len1, containsv1, min1, max1):
    MIN = 32767
    MAX = -32768
    len_post = (len1 == len - 1)
    containsv_post = Or(containsv1 == 0, containsv1 == 1)
    
    final_cond = And(min1 == MIN, max1 == MAX)
    loop_cond = And(min1 == v + 1, max1 == max)
    min_max_post = If(len1 == 0, final_cond, loop_cond)
    
    return And(len_post, containsv_post, min_max_post)

def reserve(len, N, len1):
    return And(len == 0, len1 == N)