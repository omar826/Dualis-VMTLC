# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
def insertHead(k, len, len1):
    return len1 == len + 1

def popHead(len, ret1, len1):
    return If(len > 0, len1 == len - 1, len1 == len)

def inv1(k, N, len):
    return And(k == len, k <= N, N > 0)

def inv2(len, items_processed, N):
    return And(len + items_processed == N, len >= 0)