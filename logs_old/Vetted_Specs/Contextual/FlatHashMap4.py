# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
from z3 import *

def inv1(i, N, len, containsk):
    return And(N > 1, len == i, i >= 0, i <= N, If(i == 0, containsk == 0, containsk == 1))

def inv2(i, N, len, containsk, flag, ret):
    # ret is the key of the last erased element. Erasures happen on odd i's.
    # The last odd number before i is i-1 if i is even, and i-2 if i is odd.
    # This can be expressed as i - 1 - (i % 2).
    # This relation only holds after the first erasure (at i=1), so for i>=2.
    last_erased_key = i - 1 - (i % 2)
    return And(
        N > 1,
        len == N - (i / 2),
        i >= 0,
        i <= N,
        flag == i % 2,
        containsk == 1,
        If(i >= 2, ret == last_erased_key, True)
    )

def insert(k, v, len, containsk, len1, containsk1):
    return And(len1 == len + 1, containsk1 == 1)

def erase(k, len, flag, len1, ret1):
    return And(len1 == len - 1, ret1 == k)