# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
from z3 import *

def inv(val, max):
  return And(val >= 0, val <= 3, max == val)

def push(val, max, max1):
  return max1 == If(val > max, val, max)