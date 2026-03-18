# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
def insert(i, isHeap, len, isHeap1, len1):
    return And(isHeap1 == 1, len1 == len + 1)

def deleteMin(len, isHeap, len1, ret1, isHeap1):
    return If(len > 0,
              len1 == len - 1,
              And(len1 == len, isHeap1 == isHeap))

def downHeap(isHeap2):
    return isHeap2 == 1

def inv1(i, N, isHeap, len):
    return And(i <= N, isHeap == 1, len == i)