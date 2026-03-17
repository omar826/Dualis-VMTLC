# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
def insert(k, v, len, containsk, len1, containsk1):
    return And(
        If(containsk == 0, len1 == len + 1, len1 == len),
        containsk1 == 1
    )

def erase(k, len, flag, len1, ret1):
    MAX = 128
    return If(flag == 1,
              And(len1 == len - 1, ret1 == k),
              And(len1 == len, ret1 == MAX))

def inv1(i, N, len):
    return And(i >= 0, i <= N, len == i)

def inv2(i, N, len, flag, ret):
    MAX = 128
    return And(
        i >= 0,
        i <= N,
        flag == i % 2,
        len == N - (i / 2),
        If(i <= 1,
           ret == MAX,
           If(i % 2 == 0, ret == i - 1, ret == i - 2))
    )