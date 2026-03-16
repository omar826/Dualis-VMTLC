# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
from z3 import *

def inv1(i, N, v, countv, len):
    return And(i == countv, i == len, i <= N)

def emplace(v, countv, len, countv1, len1):
    return And(countv1 == countv + 1, len1 == len + 1)