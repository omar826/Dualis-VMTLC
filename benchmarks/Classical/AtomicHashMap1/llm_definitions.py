# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
def inv1(i, N, len, min, max):
    # This invariant captures the state of the system at the beginning of each loop iteration.
    # It has two parts: the state at the very beginning (i=0), and the state during subsequent iterations (i>0).
    
    # State before the loop starts (i=0): len is 0, and min/max have their initial sentinel values.
    initial_state = And(i == 0, len == 0, min == 128, max == -129)
    
    # State during the loop (i>0):
    # - len tracks the number of unique keys inserted, which is equal to the iteration count `i`.
    # - min is 0 because the first value inserted was 0 (from the pair (0,0)) and no smaller value is ever inserted.
    # - max is `i` because in the previous iteration (i-1), the last value inserted was `(i-1)+1 = i`.
    loop_state = And(i > 0, len == i, min == 0, max == i)
    
    # The full invariant combines these conditions and ensures `i` stays within the loop bounds.
    return And(0 <= i, i <= N, Or(initial_state, loop_state))

def insert(k, v, len, min, max, len1, min1, max1):
    # This function defines the behavior of inserting a key-value pair (k, v).
    # The specification models a data structure that assumes keys are inserted contiguously starting from 0.
    
    # The new length (len1) increases by 1 only if a new key is being added.
    # We model a "new key" condition as `k >= len`, which is true for the client's access pattern.
    # If the key is already present (k < len), it's an update, and the length does not change.
    new_len = If(k >= len, len + 1, len)
    
    # The new minimum (min1) is the smaller of the current min and the new value v.
    # It handles the special case of inserting into an empty structure (len == 0).
    new_min = If(len == 0, v, If(v < min, v, min))
    
    # The new maximum (max1) is the larger of the current max and the new value v.
    # It also handles the empty case.
    new_max = If(len == 0, v, If(v > max, v, max))
    
    return And(len1 == new_len, min1 == new_min, max1 == new_max)

def find(k, len, min, max, ret1):
    # This function defines the behavior of searching for a key `k`.
    # The specification is general enough to only constrain the success/failure outcome.
    
    # The key `k` is considered present if it's in the range [0, len-1],
    # consistent with the behavior of the specified `insert` function.
    key_is_present = And(0 <= k, k < len)
    
    # If the key is present, the return value `ret1` must not be the failure sentinel MIN (-129).
    # If the key is not present, the return value must be MIN.
    return If(key_is_present, ret1 != -129, ret1 == -129)