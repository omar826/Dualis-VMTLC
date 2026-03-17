# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
MAX = 128
MIN = -129

def inv1(i, N, len, containsv, min, max):
    loop_condition = And(i >= 0, i <= N)
    len_is_i = (len == i)
    min_max_props = If(i > 0,
                       And(min == 0, max == i - 1),
                       And(min == MAX, max == MIN))
    return And(loop_condition, len_is_i, min_max_props)

def inv2(i, N, len, containsv, min, max):
    loop_condition = And(i >= 0, i <= N)
    len_is_N_minus_i = (len == N - i)
    min_max_props = If(i < N,
                       And(min == i, max == N - 1),
                       And(min == MAX, max == MIN))
    return And(loop_condition, len_is_N_minus_i, min_max_props)

def inv3(i, N, len, containsv, min, max):
    loop_condition = And(i >= 0, i <= N)
    len_is_i = (len == i)
    min_max_props = If(i > 0,
                       And(min == N, max == i + N - 1),
                       And(min == MAX, max == MIN))
    return And(loop_condition, len_is_i, min_max_props)

def insert(v, len, containsv, min, max, len1, containsv1, min1, max1):
    len_update = (len1 == len + 1)
    min_update = (min1 == If(len == 0, v, If(v < min, v, min)))
    max_update = (max1 == If(len == 0, v, If(v > max, v, max)))
    return And(len_update, min_update, max_update)

def erase(v, len, containsv, min, max, len1, containsv1, min1, max1):
    len_update = (len1 == If(len > 0, len - 1, 0))
    min_update = (min1 == If(len <= 1, MAX, If(v == min, min + 1, min)))
    max_update = (max1 == If(len <= 1, MIN, If(v == max, max - 1, max)))
    return And(len_update, min_update, max_update)

def reserve(len, N, len1):
    return len1 == len

def fail():
    return False