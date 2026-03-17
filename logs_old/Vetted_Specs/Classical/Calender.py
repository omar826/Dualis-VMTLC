# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
def inv(len, maxDiff):
  return And(len >= 0, If(len > 0, maxDiff < 2, maxDiff == 0))

def insert(len, len1, ev1, ev2, maxDiff, maxDiff1):
  absl_diff = If(ev1 - ev2 >= 0, ev1 - ev2, -(ev1 - ev2))
  new_maxDiff = If(maxDiff > absl_diff, maxDiff, absl_diff)
  return And(len1 == len + 1, maxDiff1 == new_maxDiff)