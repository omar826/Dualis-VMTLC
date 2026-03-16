# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
from z3 import *

def inv(inserted_blue, bcount, color):
    # This invariant captures the core logic from the abstract program:
    # (inserted_blue == false ==> bcount == 0) && (inserted_blue == true ==> bcount == 1)
    # Booleans are modeled as 0/1 integers.
    ib_is_false = (inserted_blue == 0)
    bc_is_zero = (bcount == 0)
    ib_is_true = (inserted_blue == 1)
    bc_is_one = (bcount == 1)
    
    # The 'color' argument is part of the state for the CHC solver but not needed
    # for defining the invariant property on 'inserted_blue' and 'bcount'.
    return And(Implies(ib_is_false, bc_is_zero), Implies(ib_is_true, bc_is_one))

def push(color, bcount, bcount1):
    # This relation defines the state transition for bcount when a blue item is pushed.
    # From the abstract program comment: "color == blue ==> bcount' = bcount + 1"
    # Assuming blue is represented by color == 0.
    # The comment also implies "color != blue ==> bcount' = bcount".
    return bcount1 == If(color == 0, bcount + 1, bcount)

def push1(color, bcount, bcount1):
    # This relation corresponds to the "else if (color == white)" branch.
    # In this branch, the abstract program indicates no change to bcount.
    # Therefore, the next state of bcount is the same as the current state.
    return bcount1 == bcount