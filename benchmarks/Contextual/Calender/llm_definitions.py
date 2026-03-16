# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
from z3 import *

def inv(len, maxDiff):
  # The invariant has two parts:
  # 1. 'len' starts at 0 and is only incremented, so it's always non-negative.
  # 2. 'maxDiff' starts at 0 (defined by INT_MIN) and is updated with the max
  #    of its current value and abs(ev1 - ev2). The program logic ensures that
  #    abs(ev1 - ev2) is always less than 2. Therefore, maxDiff itself will
  #    always be less than 2.
  return And(len >= 0, maxDiff < 2)

def insert(len, len1, ev1, ev2, maxDiff, maxDiff1):
  # This relation models the state update inside the 'if' block.
  # 'len' is incremented.
  len_update = (len1 == len + 1)

  # 'maxDiff' is updated to be the maximum of its previous value and the
  # new absolute difference between ev1 and ev2.
  # We model max(a, b) using Z3's If expression: If(a > b, a, b).
  # We model abs(x) using Z3's If expression: If(x >= 0, x, -x).
  current_diff = If(ev1 - ev2 >= 0, ev1 - ev2, -(ev1 - ev2))
  maxDiff_update = (maxDiff1 == If(maxDiff > current_diff, maxDiff, current_diff))

  return And(len_update, maxDiff_update)