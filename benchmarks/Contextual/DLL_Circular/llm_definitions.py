# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
from z3 import *

def inv(val, max):
  """
  Defines the loop invariant.
  It must hold at the beginning of the loop and be preserved by each iteration.
  Based on the abstract program, 'val' ranges from 0 to 3. 'max' tracks
  the maximum value 'val' has reached.
  So, the invariant states:
  1. val is non-negative (val >= 0).
  2. val is always less than or equal to max (val <= max).
  3. max never exceeds 3 (max <= 3).
  These three conditions together imply 0 <= val <= max <= 3.
  """
  return And(val >= 0, val <= max, max <= 3)

def push(val, max, max1):
  """
  Defines the state transition for the 'max' variable.
  The 'push' operation updates 'max' to be the maximum of its current value
  and the current value of 'val'.
  'max1' represents the next state of 'max'.
  The relation is max1 == if (val > max) then val else max.
  """
  return max1 == If(val > max, val, max)