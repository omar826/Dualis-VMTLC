# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
def inv1(i, N, len, min, max):
    return And(i >= 0, i <= N, len == i, If(i > 0, And(min == 0, max == i - 1), And(min == 128, max == -129)))

def insert(k, v, len, min, max, len1, min1, max1):
    is_empty = (len == 0)
    insert_into_empty = And(len1 == 1, min1 == k, max1 == k)

    # Non-empty cases:
    is_dense = (len == max - min + 1)
    is_within_bounds = And(k >= min, k <= max)
    
    # Behavior when a new key is added that expands the bounds
    append_behavior = And(len1 == len + 1,
                          min1 == If(k < min, k, min),
                          max1 == If(k > max, k, max))
    
    # Behavior when the key is within the current bounds and is just an update
    update_behavior = And(len1 == len, min1 == min, max1 == max)

    # If the key set is dense, any key within bounds is an update. Outside is an append.
    dense_logic = If(is_within_bounds, update_behavior, append_behavior)

    # If the key set is sparse, a key outside is an append. A key inside could be an
    # update OR a new key in a gap (which increases len but not bounds).
    sparse_logic = If(Not(is_within_bounds),
                      append_behavior,
                      Or(
                          update_behavior,
                          And(len1 == len + 1, min1 == min, max1 == max)
                      ))

    return If(is_empty,
              insert_into_empty,
              If(is_dense, dense_logic, sparse_logic))

def find(k, len, min, max, ret1):
    return If(And(len > 0, min <= k, k <= max), ret1 != -129, True)