# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
def insert(i, isHeap, len, isHeap1, len1):
    return And(len1 == len + 1, isHeap1 >= isHeap, Or(isHeap1 == 0, isHeap1 == 1))

def deleteMin(len, isHeap, len1, ret1, isHeap1):
    return And(
        Implies(len > 0, len1 == len - 1),
        Implies(len <= 0, len1 == len)
    )

def downHeap(isHeap2):
    return isHeap2 == 1

def inv1(i, N, isHeap, len):
    return And(i >= 0, i <= N, len == i, isHeap == 1)