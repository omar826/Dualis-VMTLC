# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
def inv(len, min, max):
    initial_state = And(len == 0, min == 128, max == -129)
    loop_state = And(len > 0, min == 0, max == 0)
    return Or(initial_state, loop_state)

def push(val, min, len, max, min1, len1, max1):
    return And(len1 == len + 1,
               min1 == If(val < min, val, min),
               max1 == If(val > max, val, max))