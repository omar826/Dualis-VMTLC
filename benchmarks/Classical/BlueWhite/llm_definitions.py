# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
def inv(inserted_blue, bcount, color):
    # if blue has not been inserted (inserted_blue == 0), then blue_count must be 0
    cond_not_inserted = Implies(inserted_blue == 0, bcount == 0)
    # if blue has been inserted (inserted_blue == 1), then blue_count must be 1
    cond_inserted = Implies(inserted_blue == 1, bcount == 1)
    return And(cond_not_inserted, cond_inserted)

def push(color, bcount, bcount1):
    # blue is represented by color 0.
    # If the color is blue (0), the new blue count is the old count + 1.
    # Otherwise, the count remains unchanged.
    return If(color == 0, bcount1 == bcount + 1, bcount1 == bcount)