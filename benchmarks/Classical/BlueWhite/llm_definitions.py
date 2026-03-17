# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
from z3 import *

def inv(inserted_blue, bcount, color):
  """
  Defines the loop invariant.
  The invariant states that the blue count (`bcount`) is 1 if and only if
  a blue item has been inserted (`inserted_blue` is true), and 0 otherwise.
  Assuming `inserted_blue` is 1 for true and 0 for false, this simplifies
  to `inserted_blue == bcount`.
  The `color` parameter is for the non-deterministic choice of the next
  iteration and does not affect the property of the current state.
  """
  return And(
    Implies(inserted_blue == 0, bcount == 0),
    Implies(inserted_blue == 1, bcount == 1)
  )

def push(color, bcount, bcount1):
  """
  Defines the behavior of the push operation.
  If the color being pushed is blue (represented by 0), the blue count is incremented.
  For any other color, the blue count remains unchanged.
  """
  return If(color == 0, bcount1 == bcount + 1, bcount1 == bcount)