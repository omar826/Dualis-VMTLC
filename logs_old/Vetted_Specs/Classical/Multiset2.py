# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
from z3 import *

# Function definitions below

def inv1(i, N, v, countvo, countvt, len):
    """
    Loop invariant for the first loop.
    - i: loop counter, ranges from 0 to N.
    - N: loop bound.
    - v: value being inserted in the loop (always 1).
    - countvo: count of value 1.
    - countvt: count of value 2.
    - len: total number of elements.
    The invariant states that after 'i' iterations:
    - The number of elements 'len' is equal to 'i'.
    - The count of '1's, 'countvo', is equal to 'i'.
    - The count of '2's, 'countvt', is 0.
    - The value 'v' used within the loop context is 1.
    - The loop counter 'i' is between 0 and N (inclusive).
    """
    return And(i <= N, i >= 0, v == 1, len == i, countvo == i, countvt == 0)

def emplace(v, countvo, countvt, len, countvo1, countvt1, len1):
    """
    Models the behavior of adding an element 'v' to a collection.
    - v: the value to be added.
    - countvo, countvt, len: current state variables.
    - countvo1, countvt1, len1: next state variables.
    The specification is general:
    - The total length always increases by 1.
    - If the inserted value 'v' is 1, 'countvo' is incremented.
    - If the inserted value 'v' is 2, 'countvt' is incremented.
    - Otherwise, the counts remain unchanged.
    """
    return And(
        len1 == len + 1,
        countvo1 == If(v == 1, countvo + 1, countvo),
        countvt1 == If(v == 2, countvt + 1, countvt)
    )