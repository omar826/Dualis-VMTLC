# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
from z3 import *

def inv(inserted_blue, bcount, color):
    # This invariant captures the core logic of the client program:
    # If blue has not been inserted (inserted_blue == 0), the blue count must be 0.
    # If blue has been inserted (inserted_blue == 1), the blue count must be 1.
    # This property is established at initialization and preserved by all loop paths.
    
    # inserted_blue == 0 ==> bcount == 0
    cond1 = Implies(inserted_blue == 0, bcount == 0)
    
    # inserted_blue == 1 ==> bcount == 1
    cond2 = Implies(inserted_blue == 1, bcount == 1)
    
    return And(cond1, cond2)

def push(color, bcount, bcount1):
    # This function defines the general behavior of the 'push' operation.
    # It is independent of the client's state (like 'inserted_blue').
    # If the color pushed is blue (represented by 0), the count is incremented.
    # For any other color, the count remains unchanged.
    return If(color == 0, bcount1 == bcount + 1, bcount1 == bcount)