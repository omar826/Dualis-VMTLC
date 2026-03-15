# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
def inv1(i, N, len, min, max, kveq):
    n_constraint = (N > 3)
    i_in_bounds = And(0 <= i, i <= N)
    kveq_is_true = (kveq == 1)
    initial_state = And(i == 0,
                        len == 0,
                        min == 128,
                        max == -129)
    loop_state = And(i > 0,
                     len == i,
                     min == 0,
                     max == i - 1)
    return And(n_constraint, i_in_bounds, kveq_is_true, Or(initial_state, loop_state))

def inv2(i, N, len, min, max, kveq):
    n_constraint = (N > 3)
    i_in_bounds = And(0 <= i, i <= N)
    final_state = And(len == N,
                      min == 0,
                      max == N - 1,
                      kveq == 1)
    return And(n_constraint, i_in_bounds, final_state)

def insert(k, v, len, min, max, kveq, len1, min1, max1, kveq1):
    is_new_key_outside_bounds = Or(len == 0, k < min, k > max)
    is_dense_before = And(len > 0, len == max - min + 1)

    update_as_new_extreme = And(
        len1 == len + 1,
        min1 == If(len == 0, k, If(k < min, k, min)),
        max1 == If(len == 0, k, If(k > max, k, max)),
        kveq1 == If(And(kveq == 1, k == v), 1, 0)
    )

    update_as_hole_fill = And(
        len1 == len + 1,
        min1 == min,
        max1 == max,
        kveq1 == If(And(kveq == 1, k == v), 1, 0)
    )

    no_change = And(len1 == len, min1 == min, max1 == max, kveq1 == kveq)

    return If(
        is_new_key_outside_bounds,
        update_as_new_extreme,
        If(is_dense_before,
           no_change,
           Or(no_change, update_as_hole_fill)
        )
    )

def find(k, len, min, max, kveq, ret1):
    is_dense = And(len > 0, len == max - min + 1)
    is_within_bounds = And(len > 0, k >= min, k <= max)

    # This is the special case required by the client's proof context.
    # The client builds a dense structure where key == value for all elements.
    guaranteed_found = And(is_dense, kveq == 1, is_within_bounds)

    # If k is outside the [min, max] range, it definitely cannot be found.
    guaranteed_not_found = Not(is_within_bounds)

    return If(guaranteed_found,
              ret1 == k,
              If(guaranteed_not_found,
                 ret1 != k,
                 True  # For all other cases (e.g., sparse sets, or dense sets where kveq==0),
                       # the key may or may not be present, so the outcome is non-deterministic.
              )
    )