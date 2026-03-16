# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
def inv(len, min, max):
  return Or(len == 0, And(min == 0, max == 0))

def push(val, min, len, max, min1, len1, max1):
  return And(
    len1 == len + 1,
    If(len == 0,
       And(min1 == val, max1 == val),
       And(min1 == If(val < min, val, min),
           max1 == If(val > max, val, max))
    )
  )