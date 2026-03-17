# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
def inv1(i_old, N, len, min, max, kveq):
    cond_N = (N > 0)
    cond_i = And(0 <= i_old, i_old <= N)
    cond_len = (len == i_old)
    cond_min = If(i_old == 0, min == 128, min == 0)
    cond_max = If(i_old == 0, max == -129, max == i_old - 1)
    cond_kveq = (kveq == 1)
    return And(cond_N, cond_i, cond_len, cond_min, cond_max, cond_kveq)

def inv2(i, N, len, min, max, kveq):
    cond_i = And(0 <= i, i <= N)
    cond_N = (N > 0)
    cond_len = (len == N)
    cond_min = (min == 0)
    cond_max = (max == N - 1)
    cond_kveq = (kveq == 1)
    cond_dense = (len == max - min + 1)
    return And(cond_i, cond_N, cond_len, cond_min, cond_max, cond_kveq, cond_dense)

def insert(k, v, len, min, max, kveq, len1, min1, max1, kveq1):
    is_present_guess = And(len > 0, k >= min, k <= max)
    update_len = If(is_present_guess, len1 == len, len1 == len + 1)
    update_min = (min1 == If(len == 0, k, If(k < min, k, min)))
    update_max = (max1 == If(len == 0, k, If(k > max, k, max)))
    update_kveq = (kveq1 == If(And(kveq == 1, k == v), 1, 0))
    return And(update_len, update_min, update_max, update_kveq)

def find(k, len, min, max, kveq, ret1):
    is_dense = And(len > 0, len == max - min + 1)
    is_present = And(k >= min, k <= max, is_dense)
    return If(is_present, ret1 != 128, ret1 == 128)