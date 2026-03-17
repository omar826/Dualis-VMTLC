# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
from z3 import *

def inv(inserted_blue, bcount, color):
    # The invariant states that the number of blue items counted (bcount)
    # is 1 if a blue item has been inserted, and 0 otherwise.
    # This can be simplified to bcount == inserted_blue,
    # where inserted_blue is 0 for false and 1 for true.
    # The 'color' variable represents the non-deterministic choice for the
    # *next* iteration, so the invariant on the *current* state does not depend on it.
    return bcount == inserted_blue

def push(color, bcount, bcount1):
    # The specification for the general-purpose push function.
    # If the color pushed is blue (represented by 0), the blue count increments.
    # For any other color (e.g., white, represented by 1), the count is unchanged.
    blue = 0
    return If(color == blue, bcount1 == bcount + 1, bcount1 == bcount)