# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
def insertHead(k, min, max, len, min1, max1, len1):
    return And(
        len1 == len + 1,
        min1 == If(k < min, k, min),
        max1 == If(k > max, k, max)
    )

def popHead(min, max, len, min1, max1, len1, ret1):
    return And(
        len1 == len - 1,
        min1 == min,
        max1 == max,
        ret1 == If(len - 1 == 0, 0, MAX)
    )

def inv1(k, N, min, max, len):
    return And(
        k >= 0,
        k <= N,
        len == k,
        If(k == 0,
           And(min == MAX, max == MIN),
           And(min == 0, max == k - 1))
    )

def inv2(len, min, max, items_processed, ret):
    actual_len = max
    actual_min = len
    actual_max = min
    
    return And(
        actual_len >= 0,
        items_processed >= 0,
        actual_len + items_processed == actual_max + 1,
        If(actual_len > 0, actual_min == 0, True),
        If(actual_len == 0, ret == 0, ret == MAX)
    )