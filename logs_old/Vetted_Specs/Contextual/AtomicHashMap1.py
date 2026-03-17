# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
def inv1(i, N, len, min, max):
    MAX = 128
    MIN = -129
    # This invariant holds at the beginning of each loop iteration.
    # It states that the number of elements 'len' is equal to the loop counter 'i'.
    # It also defines the 'min' and 'max' key values based on 'i'.
    # For i=0 (initial state), min/max have their initial sentinel values.
    # For i>0, the keys inserted are {0, 1, ..., i-1}, so min=0 and max=i-1.
    initial_state_props = And(min == MAX, max == MIN)
    loop_state_props = And(min == 0, max == i - 1)

    return And(
        0 <= i, i <= N,
        len == i,
        If(i == 0, initial_state_props, loop_state_props)
    )

def insert(k, v, len, min, max, len1, min1, max1):
    # This relation models the insertion of a new key 'k'.
    # The length of the structure increases by one.
    # The 'min' and 'max' values are updated based on the new key 'k'.
    # If the structure was empty (len=0), min and max both become 'k'.
    # Otherwise, they are updated by taking the min/max of the old values and 'k'.
    len_is_updated = (len1 == len + 1)
    min_is_updated = If(len == 0, min1 == k, min1 == If(k < min, k, min))
    max_is_updated = If(len == 0, max1 == k, max1 == If(k > max, k, max))

    return And(len_is_updated, min_is_updated, max_is_updated)

def insert1(k, v, len, min, max, len1, min1, max1):
    # This relation models an update to an existing key 'k'.
    # Such an operation does not change the number of keys ('len'),
    # the minimum key ('min'), or the maximum key ('max').
    # Therefore, the output state is the same as the input state.
    return And(
        len1 == len,
        min1 == min,
        max1 == max
    )

def find(k, len, min, max, ret1):
    MIN = -129
    # This relation models the find operation.
    # It succeeds (ret1 != MIN) if and only if the structure is not empty (len > 0)
    # and the searched key 'k' is within the range of existing keys, [min, max].
    key_is_present = And(len > 0, min <= k, k <= max)
    
    return (ret1 != MIN) == key_is_present