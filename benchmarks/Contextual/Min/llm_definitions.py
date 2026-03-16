# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
from z3 import *

def inv(lmin, gmin, len):
    """
    Specifies the invariant for the loop.
    Based on the abstract program, both lmin and gmin track the minimum value seen so far.
    The invariant is that they must always be equal.
    - Base case: Initially, lmin = INT_MAX and gmin = INT_MAX, so lmin == gmin holds.
    - Inductive step: If lmin == gmin, then after updating both with a new value 'v',
      the new lmin1 will be min(lmin, v) and the new gmin1 will be min(gmin, v).
      Since lmin == gmin, lmin1 will equal gmin1.
    - Post-condition: The assertion requires gmin == lmin. Our invariant directly proves this.
    """
    return lmin == gmin

def append(v, lmin, lmin1, len, len1):
    """
    Specifies the behavior of the append operation.
    The abstract program shows 'append' being used to update the local minimum 'lmin'.
    When a new value 'v' is introduced, the new minimum 'lmin1' becomes the smaller
    of the current minimum 'lmin' and the new value 'v'.
    This is equivalent to lmin1 = min(lmin, v).
    """
    return lmin1 == If(v < lmin, v, lmin)