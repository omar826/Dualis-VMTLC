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
        len > 0,
        len1 == len - 1,
        If(len1 == 0,
           And(min1 == 128, max1 == -129),
           And(min1 == min, max1 == max - 1)),
        ret1 == 0
    )

def inv1(k, N, min, max, len):
    return And(
        k >= 0,
        k <= N,
        len == k,
        If(k == 0,
           And(min == 128, max == -129),
           And(min == 0, max == k - 1))
    )

def inv2(min, max, len, items_processed, ret):
    # N is a global variable available in the context of the checker
    count_prop = (len + items_processed == N)
    len_bounds = (len >= 0)
    data_prop = If(len == 0,
                   And(min == 128, max == -129),
                   And(min == 0, max == len - 1))
    ret_prop = If(items_processed == 0,
                  ret == 128,
                  ret == 0)
    return And(count_prop, len_bounds, data_prop, ret_prop)

def fail():
    return False