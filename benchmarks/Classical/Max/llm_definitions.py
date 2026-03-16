# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
from z3 import *

def inv(plmax, pgmax, plen):
  """
  Specifies the invariant relationship between the local maximum (lmax)
  and the global maximum (gmax).
  To prove the final assertion `gmax == lmax`, this invariant must
  be strong enough to imply it. The simplest such invariant is `gmax == lmax`.
  This holds at initialization (INT_MIN == INT_MIN) and is preserved
  if `append` updates `lmax` in the same way the loop body updates `gmax`.
  """
  return plmax == pgmax

def append(v1, plmax, plmax1, plen, plen1):
  """
  Specifies the behavior of the `append` function.
  It takes a value `v1` and the current local maximum `plmax`,
  and relates them to the next local maximum `plmax1`.
  The most natural interpretation is that the new local maximum `plmax1`
  is the maximum of the old local maximum and the new value.
  This mirrors the update rule for `gmax` in the client program's loop,
  which is essential for maintaining the invariant `lmax == gmax`.
  """
  return plmax1 == If(v1 > plmax, v1, plmax)