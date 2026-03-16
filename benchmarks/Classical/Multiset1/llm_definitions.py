# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
def emplace(v, countv, len, countv1, len1):
    return And(len1 == len + 1, countv1 == countv + 1)

def inv1(i, N, v, countv, len):
    return And(i <= N, len == i, countv == i)