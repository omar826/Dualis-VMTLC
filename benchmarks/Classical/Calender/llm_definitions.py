# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
from z3 import *

def inv(length, max_diff):
    """
    Loop invariant for the system.
    It captures three properties:
    1. The length is always non-negative.
    2. If the length is zero (initial state), max_diff is also zero.
    3. If the length is positive, the tracked maximum difference is less than 2.
    """
    len_non_negative = (length >= 0)
    initial_state_prop = Implies(length == 0, max_diff == 0)
    assertion_prop = Implies(length > 0, max_diff < 2)
    return And(len_non_negative, initial_state_prop, assertion_prop)

def insert(len_in, len_out, ev1, ev2, max_diff_in, max_diff_out):
    """
    Specification for the insert operation.
    It defines the state transition:
    1. The length is incremented by 1.
    2. The new max_diff is the maximum of the previous max_diff and the
       absolute difference of the new events (ev1, ev2).
    """
    # Define the update to length
    len_update = (len_out == len_in + 1)

    # Define the update to max_diff
    diff = ev1 - ev2
    abs_diff = If(diff >= 0, diff, -diff)
    new_max_diff = If(max_diff_in > abs_diff, max_diff_in, abs_diff)
    max_diff_update = (max_diff_out == new_max_diff)

    return And(len_update, max_diff_update)