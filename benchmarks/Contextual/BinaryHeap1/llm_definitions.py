# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
def inv1(i, N, isHeap, min, max, len):
    initial_cond = And(min == 128, max == -129)
    loop_cond = And(min == 0, max == i - 1)
    
    return And(
        i >= 0, i <= N,
        len == i,
        isHeap == 1,
        N > 0,
        If(i == 0, initial_cond, loop_cond)
    )

def inv2(d, N, min, max, len, isHeap, ret):
    min_cond = If(len > 0, min == d, True)
    ret_cond = ret == If(d == 0, 128, d - 1)

    return And(
        d >= 0, d <= N,
        len == N - d,
        isHeap == 1,
        N > 0,
        max == N - 1,
        min_cond,
        ret_cond
    )

def insert(i, isHeap, min, max, len, isHeap1, min1, max1, len1):
    return And(
        len1 == len + 1,
        isHeap1 == 1,
        min1 == If(len == 0, i, min),
        max1 == i
    )

def deleteMin(min, max, len, isHeap, min1, max1, len1, ret1, isHeap1):
    return And(
        len1 == len - 1,
        ret1 == min,
        max1 == max,
        isHeap1 == isHeap,
        min1 == min + 1
    )

def downHeap(isHeap2):
    return isHeap2 == 1

def fail():
    return False