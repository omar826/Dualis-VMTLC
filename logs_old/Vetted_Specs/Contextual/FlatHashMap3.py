# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
from z3 import *

def inv1(i, N, len, containsk):
    return And(i >= 0, i <= N, len == i, If(i == 0, containsk == 0, containsk == 1))

def inv2(i, N, len, containsk, flag, ret):
    num_erased = (i + (i % 2)) / 2
    return And(
        i >= 0,
        i <= N,
        containsk == If(N > 0, 1, 0),
        flag == 1 - (i % 2),
        len == N - num_erased,
        Implies(i > 0, If(i % 2 == 1, ret == i - 1, ret == i - 2))
    )

def insert(k, value, len, containsk, len1, containsk1):
    return And(len1 == len + 1, containsk1 == 1)

def erase(k, len, flag, len1, ret1):
    return And(len1 == len - 1, ret1 == k)