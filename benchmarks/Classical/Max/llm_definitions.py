# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
from z3 import *

def inv(lmax, gmax, len):
  """
  Specifies the loop invariant.
  The invariant states that the local maximum tracked by the append operation (`lmax`)
  is always equal to the global maximum (`gmax`).
  This holds because both are initialized to the same value and updated with
  identical logic in response to new values `v`.
  """
  return lmax == gmax

def append(v, lmax, lmax1, len, len1):
  """
  Specifies the behavior of the append operation, which updates the running maximum.
  Given a new value `v` and the current maximum `lmax`, the new maximum `lmax1`
  will be `v` if `v` is greater than `lmax`, otherwise it remains `lmax`.
  This is equivalent to `lmax1 = max(v, lmax)`.
  """
  return lmax1 == If(v > lmax, v, lmax)