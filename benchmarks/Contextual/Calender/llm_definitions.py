# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
from z3 import *

def inv(length, max_diff):
    """
    Defines the loop invariant for the program.
    - length must be non-negative, as it starts at 0 and only increases.
    - max_diff must be less than or equal to 1.
      This is because max_diff starts at 0 (INT_MIN in this context)
      and is only updated with the maximum of its current value and
      absl(ev1 - ev2). The loop condition `absl(ev1 - ev2) < 2` ensures
      this difference is at most 1.
    """
    return And(length >= 0, max_diff <= 1)

def insert(len_in, len_out, ev1, ev2, max_diff_in, max_diff_out):
    """
    Defines the state transition for the insert operation.
    - The length is incremented by 1.
    - The new max_diff is the maximum of the previous max_diff and the
      absolute difference between the current events ev1 and ev2.
    """
    # Calculate the absolute difference between ev1 and ev2 using If-Then-Else
    diff_val = ev1 - ev2
    abs_diff = If(diff_val >= 0, diff_val, -diff_val)

    # Define the state updates
    len_update = (len_out == len_in + 1)
    # The new max_diff is the max of the old one and the new difference
    max_diff_update = (max_diff_out == If(max_diff_in > abs_diff, max_diff_in, abs_diff))

    return And(len_update, max_diff_update)