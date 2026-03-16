# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
from z3 import *

# Helper functions if needed, or Z3 functions like If, And, Or, etc.

def inv1(i, N, v, countvo, countvt, len):
  """
  Loop invariant for the first while loop.
  - The loop counter i is between 0 and N.
  - The value v being inserted is always 1.
  - The count of '1's (countvo) is equal to the loop counter.
  - The count of '2's (countvt) is always 0 inside this loop.
  - The total length is equal to the loop counter.
  """
  return And(i >= 0, i <= N, v == 1, countvo == i, countvt == 0, len == i)

def emplace(v, countvo, countvt, len, countvo1, countvt1, len1):
  """
  Specification for the emplace function.
  - The length is always incremented by 1.
  - If the value v is 1, the count of '1's (countvo) is incremented.
  - If the value v is 2, the count of '2's (countvt) is incremented.
  - For any other value, the counts remain unchanged.
  """
  update_countvo = If(v == 1, countvo + 1, countvo)
  update_countvt = If(v == 2, countvt + 1, countvt)
  return And(
    len1 == len + 1,
    countvo1 == update_countvo,
    countvt1 == update_countvt
  )