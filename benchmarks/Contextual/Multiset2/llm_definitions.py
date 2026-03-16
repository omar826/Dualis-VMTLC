# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
from z3 import *

def inv1(i, N, v, countvo, countvt, len):
    """
    Loop Invariant for the first loop.
    This invariant must hold:
    1. Initially (Base Case, Rule 1).
    2. Be preserved by each loop iteration (Inductive Step, Rule 2).
    3. Hold at loop exit to prove the final assertion (Query, Rule 3).

    - i: loop counter, ranges from 0 to N.
    - v: value being emplaced, is constant 1 during the loop.
    - len: total elements, must equal the loop counter i.
    - countvo: count of v=1 elements, must equal the loop counter i.
    - countvt: count of v=2 elements, must remain 0 during the loop.
    - N: loop bound, must be greater than or equal to i.
    """
    return And(i >= 0, i <= N,
               v == 1,
               len == i,
               countvo == i,
               countvt == 0)

def emplace(v, countvo, countvt, len, countvo1, countvt1, len1):
    """
    Models the emplace operation called inside the loop.
    The behavior depends on the value of 'v'.
    - If v is 1, it increments countvo.
    - If v is 2, it increments countvt.
    - In all cases, it increments len.
    In the context of Rule 2, the invariant ensures v is always 1.
    """
    v1_case = And(countvo1 == countvo + 1,
                  countvt1 == countvt,
                  len1 == len + 1)

    v2_case = And(countvo1 == countvo,
                  countvt1 == countvt + 1,
                  len1 == len + 1)

    return If(v == 1, v1_case,
              If(v == 2, v2_case, False))

def emplace1(v, countvo, countvt, len, countvo1, countvt1, len1):
    """
    Models the emplace operation called after the loop.
    This relation has the same logic as emplace.
    In the context of Rule 3, 'v' (passed as v1) is explicitly 2.
    """
    v1_case = And(countvo1 == countvo + 1,
                  countvt1 == countvt,
                  len1 == len + 1)

    v2_case = And(countvo1 == countvo,
                  countvt1 == countvt + 1,
                  len1 == len + 1)

    return If(v == 1, v1_case,
              If(v == 2, v2_case, False))