# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
from z3 import *

def inv(lmax, gmax, len):
    """
    Specifies the loop invariant.
    The invariant is that the local maximum (lmax) is always equal to the global maximum (gmax).
    This holds at initialization (INT_MIN == INT_MIN) and is preserved in the loop.
    """
    return lmax == gmax

def append(v, lmax, lmax1, len, len1):
    """
    Specifies the behavior of the append operation on the local maximum.
    The new local maximum (lmax1) is the greater of the old local maximum (lmax) and the new value (v).
    This is the standard update rule for finding the maximum value in a sequence.
    """
    return lmax1 == If(v > lmax, v, lmax)