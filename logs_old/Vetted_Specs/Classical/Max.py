# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
def inv(lmax, gmax, len):
    return lmax == gmax

def append(v, lmax, lmax1, len, len1):
    return lmax1 == If(v > lmax, v, lmax)