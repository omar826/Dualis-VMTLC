# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
from z3 import *

# ==================================================================================================
#
# Note:
#
# 1. The Z3 variables (e.g., `len`, `min`, `max`) and constants (e.g., `MAX`, `MIN`)
#    are assumed to be globally available in the testing environment, as per the problem description.
#    Therefore, they are not redefined here. Their values are used directly.
#
# 2. The function signatures and parameter names are based on the `declare-rel` statements
#    and the example usage in the `rule` statements from the provided CHC.txt.
#
# ==================================================================================================


def inv1(i_old, N, len, min, max, kveq):
    """
    Invariant for the first loop. It captures the state of the data structure
    as elements (0,0), (1,1), ..., (i_old-1, i_old-1) are inserted.
    - i_old: The loop counter, from 0 to N.
    - len: The number of elements, which is equal to i_old.
    - min: The minimum key inserted so far. It is 0 once the first element is in.
    - max: The maximum key inserted so far, which is i_old-1.
    - kveq: Flag indicating if k==v, always 1 in this context.
    - N: The total number of iterations, must be positive.
    """
    # Using numeric literals 128 for MAX and -129 for MIN as defined in the CHC.
    initial_min = 128
    initial_max = -129
    
    return And(
        N > 0,
        i_old >= 0,
        i_old <= N,
        len == i_old,
        min == If(i_old == 0, initial_min, 0),
        max == If(i_old == 0, initial_max, i_old - 1),
        kveq == 1
    )

def inv2(i, N, len, min, max, kveq):
    """
    Invariant for the second loop. This loop re-inserts existing keys.
    The state of the data structure is static throughout this loop,
    reflecting the state after the first loop has completed.
    - i: The loop counter, from 0 to N.
    - len: The number of elements, fixed at N.
    - min: The minimum key, fixed at 0.
    - max: The maximum key, fixed at N-1.
    - kveq: Flag indicating if k==v, always 1 in this context.
    - N: The total number of iterations, must be positive.
    """
    return And(
        N > 0,
        i >= 0,
        i <= N,
        len == N,
        min == 0,
        max == N - 1,
        kveq == 1
    )

def insert(k, v, len, min, max, kveq, len1, min1, max1, kveq1):
    """
    Models the 'insert' operation for the first loop, where each inserted key is new.
    - len1: The length increases by 1.
    - min1, max1: The min/max values are updated with the new key k.
    - kveq1: Is 1 if k==v, 0 otherwise.
    """
    return And(
        len1 == len + 1,
        min1 == If(k < min, k, min),
        max1 == If(k > max, k, max),
        kveq1 == If(k == v, 1, 0)
    )

def insert1(k, v, len, min, max, kveq, len1, min1, max1, kveq1):
    """
    Models the 'insert' operation for the second loop, where keys are re-inserted.
    Since the keys already exist, the state of the data structure does not change.
    - len1, min1, max1: Remain the same as the input values.
    - kveq1: Is 1 if k==v, 0 otherwise.
    """
    return And(
        len1 == len,
        min1 == min,
        max1 == max,
        kveq1 == If(k == v, 1, 0)
    )

def find(k, len, min, max, kveq, ret1):
    """
    Models the 'find' operation.
    For this program, the inserted keys are a contiguous range [0, N-1].
    Therefore, a key 'k' exists if and only if it is within the range [min, max].
    - ret1: The return value. Equals the key 'k' on success (since v=k),
            and MAX (128) on failure.
    """
    # Using numeric literal 128 for MAX.
    return If(
        And(k >= min, k <= max, len > 0),
        ret1 == k,
        ret1 == 128
    )