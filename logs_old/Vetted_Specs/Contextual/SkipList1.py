# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
from z3 import *

def inv1(i, N, isPresent, min, max, len):
    """
    Invariant for the main loop.
    It captures the state of the variables (i, isPresent, min, max, len)
    at the beginning of each loop iteration, in relation to N.
    """
    # These constants are defined in the CHC file.
    MAX = 128
    MIN = -129
    
    i_is_0 = (i == 0)
    
    # At iteration i, elements 0, 1, ..., i-1 have been inserted.
    # Therefore, at the start of iteration i:
    # 1. The loop counter is between 0 and N.
    # 2. The number of elements inserted (len) is equal to the loop counter (i).
    # 3. 'isPresent' is 0 only at the very beginning (i=0), otherwise it's 1.
    # 4. 'min' is the initial MAX value at i=0. For i>0, it's 0 (the first element inserted).
    # 5. 'max' is the initial MIN value at i=0. For i>0, it's i-1 (the last element inserted).
    return And(
        i >= 0,
        i <= N,
        len == i,
        isPresent == If(i_is_0, 0, 1),
        min == If(i_is_0, MAX, 0),
        max == If(i_is_0, MIN, i - 1)
    )

def insert(i, isPresent, min, max, len, isPresent1, min1, max1, len1):
    """
    Relational specification for the insert operation.
    It relates the pre-state (isPresent, min, max, len) to the
    post-state (isPresent1, min1, max1, len1) after inserting value i.
    """
    # The new length is the old length plus one.
    len_update = (len1 == len + 1)
    
    # After any insertion, the 'isPresent' flag becomes 1.
    isPresent_update = (isPresent1 == 1)
    
    # The new minimum is the minimum of the current minimum and the inserted value i.
    min_update = (min1 == If(i < min, i, min))
    
    # The new maximum is the maximum of the current maximum and the inserted value i.
    max_update = (max1 == If(i > max, i, max))
    
    return And(len_update, isPresent_update, min_update, max_update)

def remove(k, len, len1, ret1):
    """
    Relational specification for the remove operation.
    The client program's final assertion is `len1 == len - 1`.
    The CHC 'fail' rule is triggered if `remove` is true AND `len1 != len - 1`.
    To make this rule's antecedent always false, and thus the rule valid,
    this relation must enforce that `len1 == len - 1` is always true.
    The other arguments `k` and `ret1` are unconstrained by the CHC rules.
    """
    return (len1 == len - 1)