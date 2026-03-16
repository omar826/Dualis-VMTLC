# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
from z3 import *

def inv1(c, n, d, sl):
  return And(c <= n, sl == c, d == 0, c >= 0)

def inv2(n, d, sl):
  return And(sl + d == n, sl >= 0)

def pu(n, sl, sl1):
  return sl1 == sl + 1

def po(sl, sl1):
  return sl1 == sl - 1