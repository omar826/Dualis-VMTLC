# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
from z3 import *

def inv1(i, N, len):
  """
  Loop invariant for the first loop.
  - len == i: At the start of each iteration i, N items have been inserted.
  - i >= 0: Loop counter is non-negative.
  - i <= N: Loop counter does not exceed N.
  """
  return And(len == i, i >= 0, i <= N)

def insert(k, v, len, containsk, len1, containsk1):
  """
  Specification for a general insert function.
  - If the key is not present (containsk == 0), the length increases by 1,
    and the key is now considered present (containsk1 == 1).
  - If the key is already present (containsk != 0), the length remains the same (e.g., value update),
    and the key remains present (containsk1 == 1).
  """
  return If(
      containsk == 0,
      And(len1 == len + 1, containsk1 == 1),
      And(len1 == len, containsk1 == 1)
  )

def remove_all(len, remove_count, len1, remove_count1):
  """
  Specification for a function that removes all elements.
  - The new length (len1) becomes 0.
  - The new remove count (remove_count1) is the original count plus the number of
    elements that were present (len).
  """
  return And(len1 == 0, remove_count1 == remove_count + len)