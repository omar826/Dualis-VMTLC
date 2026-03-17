# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
def inv1(i, N, isPresent, min, max, len):
    MAX = 128
    MIN = -129
    
    initial_state = And(isPresent == 0, len == 0, min == MAX, max == MIN)
    loop_state = And(isPresent == 1, len == 1, min == 1, max == 1)
    
    return And(
        i >= 0,
        i <= N,
        If(i == 0, initial_state, loop_state)
    )

def insert(v, isPresent, min, max, len, isPresent1, min1, max1, len1):
    # In the context of the program, the insert operation is always called with v=1.
    # After the first insertion, the state of the set becomes {1}, and subsequent
    # insertions of 1 are no-ops, leaving the state as {1}.
    # Therefore, the post-state of any insert(1,...) operation is always the same.
    return And(v == 1, isPresent1 == 1, len1 == 1, min1 == 1, max1 == 1)

def remove(k, len, len1, ret1):
    # The program calls remove(k, len, ...) only after the loop.
    # From the invariant inv1, we know at loop exit that len is 1.
    # The program also sets k=1.
    # This relation specifies that removing k=1 from a set of len=1 results in len1=0.
    return And(k == 1, len == 1, len1 == 0)