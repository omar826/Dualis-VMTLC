# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
from z3 import *

def inv1(i_loop, N, max, min, len, noDup):
    """
    Loop invariant for the main loop.
    It captures the state of the variables after i_loop iterations.
    - len should be equal to the number of iterations.
    - min should be 0 if any element has been inserted, otherwise the initial value.
    - max should be i_loop-1 if any element has been inserted, otherwise the initial value.
    - noDup remains true.
    - i_loop is bounded by 0 and N.
    """
    len_is_correct = (len == i_loop)
    min_is_correct = If(i_loop == 0, min == 10, min == 0)
    max_is_correct = If(i_loop == 0, max == -10, max == i_loop - 1)
    noDup_is_true = (noDup == 1)
    bounds_are_correct = And(i_loop >= 0, i_loop <= N)
    
    return And(len_is_correct, min_is_correct, max_is_correct, noDup_is_true, bounds_are_correct)

def insert(i_loop, max, min, len, noDup, max1, min1, len1, noDup1):
    """
    Models the insertion of the element 'i_loop'.
    - The new length (len1) is the old length (len) + 1.
    - The new maximum (max1) is the maximum of the old max and i_loop.
    - The new minimum (min1) is the minimum of the old min and i_loop.
    - The noDup property is preserved.
    """
    next_len = (len1 == len + 1)
    next_max = (max1 == If(i_loop > max, i_loop, max))
    next_min = (min1 == If(i_loop < min, i_loop, min))
    next_noDup = (noDup1 == noDup)
    
    return And(next_len, next_max, next_min, next_noDup)

def search(data, min, max, len, ret1):
    """
    Models the search operation.
    The search is successful (returns 1) if the data is within the range
    of the minimum and maximum elements seen so far. Otherwise, it fails (returns 0).
    """
    return (ret1 == If(And(data >= min, data <= max), 1, 0))