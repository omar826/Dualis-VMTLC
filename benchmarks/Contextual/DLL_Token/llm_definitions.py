# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
from z3 import *

# Pre-defined global constants based on CHC 'define-fun'
MAX = 128
MIN = -129

def inv(len, min, max):
  """
  Defines the loop invariant for the program.
  The program can be in one of two states:
  1. The initial empty state: length is 0, min is MAX, max is MIN.
  2. A state after pushing one or more 0s: length is positive, min is 0, max is 0.
  """
  initial_state = And(len == 0, min == MAX, max == MIN)
  loop_state = And(len > 0, min == 0, max == 0)
  return Or(initial_state, loop_state)

def push(val, min, len, max, min1, len1, max1):
  """
  Defines the state transition for the push operation.
  - The length always increases by 1.
  - If the collection was empty (len == 0), the new min and max are both equal to the pushed value.
  - If the collection was not empty, the new min and max are updated accordingly.
  """
  # Logic for updating min and max when the collection is not empty
  updated_min = If(val < min, val, min)
  updated_max = If(val > max, val, max)

  # The full transition relation
  return And(
    len1 == len + 1,
    If(
      len == 0,
      # Case for the first element being added
      And(min1 == val, max1 == val),
      # Case for adding to a non-empty collection
      And(min1 == updated_min, max1 == updated_max)
    )
  )