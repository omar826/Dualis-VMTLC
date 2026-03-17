# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
def inv1(c, n, d, sl):
  return And(c >= 0, c <= n, d == 0, sl == c)

def inv2(n, d, sl):
  return And(sl >= 0, d >= 0, sl + d == n)

def pu(n, sl, sl1):
  return sl1 == sl + 1

def po(sl, sl1):
  return sl1 == sl - 1