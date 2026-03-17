# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
from z3 import And, Or, If, Implies

def inv1(i, N, len, min, max, kveq):
    MAX = 128
    MIN = -129
    CAPACITY = MAX - 1
    
    # At the start of iteration i, we have inserted i elements (0 to i-1)
    # unless capacity was hit.
    current_len = If(i > CAPACITY, CAPACITY, i)
    current_max = If(i > CAPACITY, CAPACITY - 1, i - 1)
    
    return And(
        i >= 0, i <= N, N > 0,
        kveq == 1,
        Or(
            And(i == 0, len == 0, min == MAX, max == MIN),
            And(i > 0,
                len == current_len,
                min == 0,
                max == current_max)
        )
    )

def inv2(i, N, len, min, max, kveq):
    MAX = 128
    MIN = -129
    CAPACITY = MAX - 1

    # This invariant describes the state after loop 1 finishes (i.e., at i=N)
    # and during loop 2. This state is fixed.
    final_len = If(N > CAPACITY, CAPACITY, N)
    final_max = If(N > CAPACITY, CAPACITY - 1, N - 1)

    return And(
        i >= 0, i <= N, N > 0,
        kveq == 1,
        # N>0 implies loop1 ran at least once, so the list is not empty.
        len == final_len,
        min == 0,
        max == final_max
    )

def insert(k, v, len, min, max, kveq, len1, min1, max1, kveq1):
    MAX = 128
    MIN = -129
    CAPACITY = MAX - 1
    
    kveq_relation = (kveq1 == 1)

    is_existing = And(len > 0, k >= min, k <= max)

    update_if_existing = And(len1 == len, min1 == min, max1 == max)

    insert_if_capacity = And(
        len < CAPACITY,
        len1 == len + 1,
        min1 == If(len == 0, k, If(k < min, k, min)),
        max1 == If(len == 0, k, If(k > max, k, max))
    )
    
    fail_if_no_capacity = And(
        len >= CAPACITY,
        len1 == len,
        min1 == min,
        max1 == max
    )
    
    handle_new_key = Or(insert_if_capacity, fail_if_no_capacity)

    return And(kveq_relation, If(is_existing, update_if_existing, handle_new_key))

def insert1(k, v, len, min, max, kveq, len1, min1, max1, kveq1):
    MAX = 128
    MIN = -129
    CAPACITY = MAX - 1
    
    kveq_relation = (kveq1 == 1)

    is_existing = And(len > 0, k >= min, k <= max)

    update_if_existing = And(len1 == len, min1 == min, max1 == max)

    insert_if_capacity = And(
        len < CAPACITY,
        len1 == len + 1,
        min1 == If(len == 0, k, If(k < min, k, min)),
        max1 == If(len == 0, k, If(k > max, k, max))
    )
    
    fail_if_no_capacity = And(
        len >= CAPACITY,
        len1 == len,
        min1 == min,
        max1 == max
    )
    
    handle_new_key = Or(insert_if_capacity, fail_if_no_capacity)

    return And(kveq_relation, If(is_existing, update_if_existing, handle_new_key))

def find(k, len, min, max, kveq, ret1):
    key_is_present = And(len > 0, k >= min, k <= max)
    
    return Implies(
        And(key_is_present, kveq == 1),
        ret1 == k
    )