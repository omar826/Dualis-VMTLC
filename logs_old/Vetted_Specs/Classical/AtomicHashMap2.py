# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
def inv1(i, N, len, min, max, kveq):
    initial_cond = And(len == 0, min == 128, max == -129)
    loop_cond = And(len == i, min == 0, max == i - 1)
    return And(
        N > 3,
        i >= 0,
        i <= N,
        kveq == 1,
        If(i == 0, initial_cond, loop_cond)
    )

def inv2(i, N, len, min, max, kveq):
    return And(
        N > 3,
        i >= 0,
        i <= N,
        kveq == 1,
        min == 0,
        max == N - 1,
        len >= N,
        len <= N + i
    )

def insert(k, v, len, min, max, kveq, len1, min1, max1, kveq1):
    min_logic = If(len == 0, k, If(k < min, k, min))
    max_logic = If(len == 0, k, If(k > max, k, max))
    add_tuple = And(
        len1 == len + 1,
        min1 == min_logic,
        max1 == max_logic,
        kveq1 == If(And(kveq == 1, k == v), 1, 0)
    )

    is_update_precond = And(len > 0, min <= k, k <= max)
    update_tuple = And(
        len1 == len,
        min1 == min,
        max1 == max,
        kveq1 == kveq
    )

    return Or(add_tuple, And(is_update_precond, update_tuple))


def find(k, len, min, max, kveq, ret1):
    is_dense = (len >= max - min + 1)
    precondition_for_guaranteed_success = And(kveq == 1, len > 0, min <= k, k <= max, is_dense)
    return Implies(precondition_for_guaranteed_success, ret1 == k)