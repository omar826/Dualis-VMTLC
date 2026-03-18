# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
from z3 import *

def inv(lmin, gmin, len):
  """
  Specifies the loop invariant.
  The invariant is that the minimum calculated by the 'append' function (`lmin`)
  is always equal to the minimum calculated by the explicit if-statement (`gmin`).
  """
  return lmin == gmin

def append(v, lmin, lmin1, len, len1):
  """
  Specifies the behavior of the 'append' function.
  It models updating a running minimum. The new minimum `lmin1` is the
  smaller of the new value `v` and the old minimum `lmin`.
  """
  return lmin1 == If(v < lmin, v, lmin)