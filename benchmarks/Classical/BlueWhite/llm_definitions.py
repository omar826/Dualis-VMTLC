# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
from z3 import *

def inv(inserted_blue, bcount, color):
    # This invariant captures the core logic:
    # If a blue item has not been inserted (inserted_blue == 0), then the blue count must be 0.
    # If a blue item has been inserted (inserted_blue == 1), then the blue count must be 1.
    return And(Implies(inserted_blue == 0, bcount == 0),
               Implies(inserted_blue == 1, bcount == 1))

def push(color, bcount, bcount1):
    # This function defines the behavior of the 'push' operation.
    # If the color is blue (represented by 0), the blue count is incremented.
    # For any other color, the blue count remains unchanged.
    return If(color == 0, bcount1 == bcount + 1, bcount1 == bcount)