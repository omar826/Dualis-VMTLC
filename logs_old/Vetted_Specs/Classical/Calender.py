# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
def inv(len, maxDiff):
    return And(len >= 0,
               Implies(len == 0, maxDiff == 0),
               Implies(len > 0, maxDiff < 2))

def insert(len, len1, ev1, ev2, maxDiff, maxDiff1):
    new_diff = If(ev1 - ev2 >= 0, ev1 - ev2, -(ev1 - ev2))
    update_max_diff = If(new_diff > maxDiff, new_diff, maxDiff)
    
    return And(len1 == len + 1,
               maxDiff1 == update_max_diff)