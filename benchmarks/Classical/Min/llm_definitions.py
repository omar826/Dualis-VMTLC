# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
from z3 import *

def inv(lmin, gmin, length):
  """
  The invariant states that the minimum value tracked by the 'append' function
  is always equal to the globally tracked minimum.
  """
  return lmin == gmin

def append(v1, lmin_in, lmin_out, len_in, len_out):
  """
  The 'append' function models the update of a running minimum.
  The output minimum (lmin_out) is the smaller of the new value (v1)
  and the previous input minimum (lmin_in).
  """
  return lmin_out == If(v1 < lmin_in, v1, lmin_in)