# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
def inv1(i, N, len, containsv, min, max):
    MAX = -129
    MIN = 128
    is_empty = And(min == MIN, max == MAX)
    is_not_empty = And(min == 0, max == i - 1)
    return And(i >= 0, i <= N, len == i, If(i == 0, is_empty, is_not_empty), Or(containsv == 0, containsv == 1))

def inv2(i, N, len, containsv, min, max):
    MAX = -129
    MIN = 128
    is_empty = And(min == MIN, max == MAX)
    is_not_empty = And(min == i, max == N - 1)
    return And(i >= 0, i <= N, len == N - i, If(len == 0, is_empty, is_not_empty), Or(containsv == 0, containsv == 1))

def inv3(i, N, len, containsv, min, max):
    MAX = -129
    MIN = 128
    is_empty = And(min == MIN, max == MAX)
    is_not_empty = And(min == N, max == N + i - 1)
    return And(i >= 0, i <= N, len == i, If(i == 0, is_empty, is_not_empty), Or(containsv == 0, containsv == 1))

def insert(v, len, containsv, min, max, len1, containsv1, min1, max1):
    post_len = (len1 == len + 1)
    post_containsv = (containsv1 == 1)
    post_min = (min1 == If(len == 0, v, If(v < min, v, min)))
    post_max = (max1 == If(len == 0, v, If(v > max, v, max)))
    return And(post_len, post_containsv, post_min, post_max)

def erase(v, len, containsv, min, max, len1, containsv1, min1, max1):
    MAX = -129
    MIN = 128
    post_len = (len1 == len - 1)
    post_containsv = (containsv1 == 0)
    post_min = If(len1 == 0, min1 == MIN, min1 == v + 1)
    post_max = If(len1 == 0, max1 == MAX, max1 == max)
    return And(post_len, post_containsv, post_min, post_max)

def reserve(len, N, len1):
    return len1 == len