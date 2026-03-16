# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
def inv(len, minDiff):
  return And(len >= 0, minDiff >= 0)

def addStockOrder(stock, order, len, minDiff, len1, minDiff1):
  diff = stock - order
  return And(len1 == len + 1,
             minDiff1 == If(diff < minDiff, diff, minDiff))