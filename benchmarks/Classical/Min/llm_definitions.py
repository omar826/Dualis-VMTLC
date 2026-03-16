# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
from z3 import *

def inv(lmin, gmin, len):
  """
  Invariant relation.
  This invariant states that the local minimum 'lmin' tracked by the 'append' function
  is always equal to the global minimum 'gmin' tracked by the main loop.
  """
  return lmin == gmin

def append(v, lmin, lmin1, len, len1):
  """
  Append operation specification.
  This function models the behavior of an operation that maintains a running minimum.
  Given a new value 'v' and the current minimum 'lmin', the next minimum 'lmin1'
  is the smaller of the two.
  """
  return lmin1 == If(v < lmin, v, lmin)