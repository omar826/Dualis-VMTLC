# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
from z3 import *

def inv1(i, N, countko, len):
  return And(i >= 0, i <= N, i == countko, i == len)

def emplace(k, v, countko, len, countko1, len1):
  return And(countko1 == countko + 1, len1 == len + 1)