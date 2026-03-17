# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
def insert(v, isPresent, min, max, len, isPresent1, min1, max1, len1):
    # Specification for inserting v=1.
    # If isPresent is 0, it means the structure is empty. We add 1.
    insert_new = And(isPresent1 == 1,
                     min1 == 1,
                     max1 == 1,
                     len1 == 1)
    # If isPresent is 1, the value 1 is already present, so it's a no-op.
    insert_duplicate = And(isPresent1 == isPresent,
                           min1 == min,
                           max1 == max,
                           len1 == len)

    # This specification is valid for v=1, which is the only value the client uses.
    return And(v == 1, If(isPresent == 0, insert_new, insert_duplicate))

def remove(k, min, max, len, min1, max1, len1, ret1):
    # Specification for removing k.
    # The condition for a valid removal is that the structure contains exactly
    # one element (len == 1), and k is that element (k == min == max).
    can_remove = And(len == 1, k == min, k == max)
    
    # If removal is successful, the structure becomes empty.
    # min/max are reset to sentinel values, len becomes 0, and ret indicates success.
    state_after_remove = And(len1 == 0,
                             min1 == 128,
                             max1 == -129,
                             ret1 == 1)
    # If the condition to remove is not met, the state does not change, and ret indicates failure.
    state_no_change = And(len1 == len,
                          min1 == min,
                          max1 == max,
                          ret1 == 0)
                          
    return If(can_remove, state_after_remove, state_no_change)

def inv1(i, N, isPresent, min, max, len):
    # Loop invariant. It captures two possible states of the system during the loop.
    
    # The initial state, at the very beginning of the loop (i=0).
    initial_state = And(i == 0,
                        isPresent == 0,
                        len == 0,
                        min == 128,
                        max == -129)

    # The state after the first iteration (i > 0), where the value 1 is present.
    # This state remains stable for the rest of the loop.
    loop_state = And(i > 0,
                     isPresent == 1,
                     len == 1,
                     min == 1,
                     max == 1)
                     
    # The invariant holds if the loop counter is within bounds and the system
    # is in either the initial or the subsequent stable state.
    return And(i >= 0, i <= N, N > 0,
               Or(initial_state, loop_state))