# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
def inv1(i, N, max, min, len, noDup):
    len_is_i = (len == i)
    i_in_bounds = And(0 <= i, i <= N)
    is_noDup = (noDup == 1)
    
    range_is_correct = If(i == 0,
                          min > max,
                          And(min == 0, max == i - 1))

    return And(len_is_i, i_in_bounds, is_noDup, range_is_correct)

def insert(i, max, min, len, noDup, max1, min1, len1, noDup1):
    len_update = (len1 == len + 1)
    max_update = (max1 == If(len == 0, i, If(i > max, i, max)))
    min_update = (min1 == If(len == 0, i, If(i < min, i, min)))

    # Specification for the noDup flag after insertion.
    # This spec is a set of constraints (implications). If a case is not
    # covered, it means any outcome is possible, making the spec general.

    # Constraint 1: If duplicates already exist, they continue to exist.
    cond1 = Implies(noDup == 0, noDup1 == 0)

    # Constraint 2: If there were no duplicates and the inserted element is
    # outside the current [min, max] range, it's guaranteed to be new,
    # so no duplicates are created. This also covers the first insert (len=0).
    cond2 = Implies(And(noDup == 1, Or(i < min, i > max)), noDup1 == 1)

    # Constraint 3: If there were no duplicates and the collection was "dense"
    # (i.e., contained every integer from min to max), then inserting an
    # element within that range MUST create a duplicate.
    cond3 = Implies(And(noDup == 1, len > 0, len == max - min + 1, i >= min, i <= max), noDup1 == 0)
    
    # The ambiguous case is when noDup=1, the collection is sparse (not dense),
    # and `i` is within [min, max]. In this case, a duplicate *may or may not*
    # be created. By not adding a constraint for this case, our specification
    # correctly allows both outcomes (noDup1=0 or noDup1=1).
    noDup_spec = And(cond1, cond2, cond3)

    return And(len_update, max_update, min_update, noDup_spec)

def search(data, min, max, len, ret1, noDup):
    # Constraint 1: If a search is successful (ret1 != 0), the element found
    # must lie within the [min, max] range of the collection. This is a weak
    # but always true property.
    must_be_in_range_if_found = Implies(ret1 != 0, And(data >= min, data <= max))

    # Constraint 2: We can make a stronger statement if we know the collection
    # is "dense" and has no duplicates. In this specific case, an element
    # exists if and only if it is within the [min, max] range.
    is_dense_and_unique = And(noDup == 1, len > 0, len == max - min + 1)
    dense_case_logic = Implies(is_dense_and_unique, 
                               (ret1 != 0) == And(data >= min, data <= max))

    # The full specification is the conjunction of all known constraints.
    return And(must_be_in_range_if_found, dense_case_logic)