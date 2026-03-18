# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
def inv1(i, N, countko, len):
  return And(i >= 0, i <= N, countko == i, len == i)

def emplace(k, v, countko, len, countko1, len1):
  return And(
      If(k == 1, countko1 == countko + 1, countko1 == countko),
      len1 == len + 1
  )