# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
from z3 import *

def inv1(i, N, len, containsk):
    return And(N > 1,
               i >= 0, i <= N,
               len == i,
               If(i == 0, containsk == 0, containsk == 1))

def inv2(i, N, len, containsk, flag, ret):
    len_prop = (len == N - (i / 2))
    flag_prop = (flag == i % 2)
    # ret holds the value of the last erased key. This is only constrained after the first erase (at i=1).
    # For i>=2, if i is even, the last erase was at i-1. ret = i-1.
    # For i>=2, if i is odd, the last erase was at i-2. ret = i-2.
    ret_prop = Or(i < 2, ret == If(i % 2 == 0, i - 1, i - 2))
    
    return And(N > 1,
               i >= 0, i <= N,
               containsk == 1,
               len_prop,
               flag_prop,
               ret_prop)

def insert(k, v, len, containsk, len1, containsk1):
    return And(len1 == len + 1, containsk1 == 1)

def erase(k, len, flag, len1, ret1):
    return And(len1 == len - 1, ret1 == k)