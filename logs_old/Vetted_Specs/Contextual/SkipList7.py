# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
from z3 import *

def inv1(i, N, isPresent, min, max, len):
    """
    Defines the loop invariant for the main loop.
    - The loop counter 'i' is always between 0 and N (inclusive).
    - At the start (i=0), the 'min' value is greater than the 'max' value
      (as they are initialized to MAX and MIN respectively).
    - After the first iteration (i > 0), the 'min' value will always be
      less than or equal to the 'max' value.
    """
    counter_bounds = And(i >= 0, i <= N)
    min_max_property = If(i == 0, min > max, min <= max)
    return And(counter_bounds, min_max_property)

def insert(v, isPresent, min, max, len, isPresent1, min1, max1, len1):
    """
    Defines the 'insert' relation, modeling the update of min/max values.
    - The next minimum 'min1' is the smaller of the input value 'v' and the current 'min'.
    - The next maximum 'max1' is the larger of the input value 'v' and the current 'max'.
    - Updates to 'isPresent' and 'len' are not constrained as they are not
      relevant to the final assertion being proved.
    """
    new_min = If(v < min, v, min)
    new_max = If(v > max, v, max)
    return And(min1 == new_min, max1 == new_max)

def lower_bound(k, lb_ret1):
    """
    Defines the 'lower_bound' relation.
    - The client program asserts that lower_bound(max) == max.
    - To make the CHC rule for failure unsatisfiable, this relation must
      enforce that the return value 'lb_ret1' is equal to the input 'k'.
    """
    return lb_ret1 == k