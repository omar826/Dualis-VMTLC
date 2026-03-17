# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
def inv1(i, N, len, min, max, kveq):
    # Invariant for the first loop (populating the structure)
    # - Loop counter i is between 0 and N.
    # - kveq is 1 because we only insert (k,v) where k=v.
    # - len equals i, as one element is added per iteration.
    # - min and max track the range [0, i-1].
    # - An initial state for i=0 is handled.
    loop_bounds = And(i >= 0, i <= N)
    len_prop = (len == i)
    key_val_prop = (kveq == 1)
    range_prop = If(i == 0,
                    And(min == 128, max == -129),
                    And(min == 0, max == i - 1))
    precond = (N > 3)
    return And(loop_bounds, len_prop, key_val_prop, range_prop, precond)

def inv2(i, N, len, min, max, kveq):
    # Invariant for the second loop and the final state.
    # After the first loop, the structure contains N elements {0, ..., N-1}.
    # This state is maintained throughout the second loop as it only re-inserts existing keys.
    # - Loop counter i is between 0 and N.
    # - The structures properties (len, min, max, kveq) are fixed.
    loop_bounds = And(i >= 0, i <= N)
    len_prop = (len == N)
    key_val_prop = (kveq == 1)
    range_prop = And(min == 0, max == N - 1)
    precond = (N > 3)
    return And(loop_bounds, len_prop, key_val_prop, range_prop, precond)

def insert(k, v, len, min, max, kveq, len1, min1, max1, kveq1):
    # Defines the state transition for an insert operation.
    
    # A key is considered new if the structure is empty or the key is outside the current [min, max] range.
    # This correctly models adding a new min or max element, which is how the client uses it.
    is_new = Or(len == 0, k < min, k > max)

    # len1 increments only if the key is new.
    cond_len = (len1 == If(is_new, len + 1, len))
    
    # min1 is updated if the structure was empty or k is a new minimum.
    cond_min = (min1 == If(len == 0, k, If(k < min, k, min)))

    # max1 is updated if the structure was empty or k is a new maximum.
    cond_max = (max1 == If(len == 0, k, If(k > max, k, max)))
    
    # kveq1 remains 1 iff kveq was 1 and the new element has k==v.
    cond_kveq = (kveq1 == If(And(kveq == 1, k == v), 1, 0))
    
    return And(cond_len, cond_min, cond_max, cond_kveq)

def find(k, len, min, max, kveq, ret1):
    # Defines the behavior of the find operation.
    # The key is considered present if the structure is not empty, has no gaps, and k is in range.
    # The "no gaps" property is captured by checking if the number of elements matches the range size.
    is_present = And(
        len > 0,
        kveq == 1,
        len == max - min + 1,
        k >= min,
        k <= max
    )
    
    # If the key is present, the function must return the key.
    # Behavior is otherwise unconstrained.
    return Implies(is_present, ret1 == k)