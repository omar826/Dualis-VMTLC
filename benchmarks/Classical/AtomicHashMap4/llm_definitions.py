# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
def inv1(i, N, len, min, max, kveq):
    initial_state = And(min == 128, max == -129)
    loop_state = And(min == 0, max == i - 1)
    return And(
        i >= 0,
        i <= N,
        kveq == 1,
        len == i,
        If(i > 0, loop_state, initial_state)
    )

def inv2(i, N, len, min, max, kveq):
    post_loop1_state = And(
        len == N,
        kveq == 1,
        If(N > 0,
           And(min == 0, max == N - 1),
           And(min == 128, max == -129))
    )
    return And(
        i >= 0,
        i <= N,
        post_loop1_state
    )

def insert(k, v, len, min, max, kveq, len1, min1, max1, kveq1):
    is_dense = And(len > 0, len == max - min + 1)
    is_in_range = And(len > 0, k >= min, k <= max)

    duplicate_behavior = And(len1 == len,
                             min1 == min,
                             max1 == max,
                             kveq1 == kveq)

    new_behavior = And(len1 == len + 1,
                       min1 == If(len == 0, k, If(k < min, k, min)),
                       max1 == If(len == 0, k, If(k > max, k, max)),
                       kveq1 == If(And(kveq == 1, k == v), 1, 0))

    return If(is_in_range,
              If(is_dense,
                 duplicate_behavior,
                 Or(duplicate_behavior, new_behavior)),
              new_behavior)

def find(k, len, min, max, kveq, ret1):
    is_findable = And(
        len > 0,
        k >= min,
        k <= max,
        len == max - min + 1,
        kveq == 1
    )
    return Implies(is_findable, ret1 == k)