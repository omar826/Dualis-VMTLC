# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
def inv1(i, N, len, min, max, kveq):
    MAX = 128
    MIN = -129
    return And(N > 0,
               i >= 0,
               i <= N,
               len == i,
               Or(kveq == 1, kveq == 0),
               min == If(i == 0, MAX, 0),
               max == If(i == 0, MIN, i - 1))

def inv2(i, N, len, min, max, kveq):
    return And(N > 0,
               i >= 0,
               i <= N,
               len == N,
               Or(kveq == 1, kveq == 0),
               min == 0,
               max == N - 1)

def insert(k, v, len, min, max, kveq, len1, min1, max1, kveq1):
    return And(len1 == len + 1,
               kveq1 == If(k == v, kveq, 0),
               min1 == If(len == 0, k, If(k < min, k, min)),
               max1 == If(len == 0, k, If(k > max, k, max)))

def insert1(k, v, len, min, max, kveq, len1, min1, max1, kveq1):
    return And(len1 == len,
               min1 == min,
               max1 == max,
               kveq1 == kveq)