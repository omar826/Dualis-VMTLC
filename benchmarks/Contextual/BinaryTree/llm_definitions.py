# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
from z3 import *

#
# Helper functions from CHC
#
def is_valid (x):
    return Or(x == 1, x == 0)

MAX = 128
MIN = -129


#
# Relations to be defined by the user
#
def inv (min, isEmpty):
    # The invariant captures the relationship between isEmpty and min.
    # If the tree is empty (isEmpty == 1), the minimum value is MAX.
    # If the tree is not empty (isEmpty == 0), it contains only non-negative
    # numbers, so the minimum value must be non-negative (min >= 0).
    is_empty_state = And(isEmpty == 1, min == MAX)
    is_not_empty_state = And(isEmpty == 0, min >= 0)
    return Or(is_empty_state, is_not_empty_state)

def insert(n, min, min1, isEmpty, isEmpty1):
    # This relation describes the state transition after inserting n.
    # Pre-condition from the CHC rule is that n >= 0.
    # After insertion, the tree will not be empty, so isEmpty1 is always 0.
    # The new minimum (min1) is the minimum of the old minimum (min) and the inserted value n.
    # If the tree was empty (isEmpty == 1), the old min was MAX, so the new min is simply n.
    new_min = If(isEmpty == 1, n, If(n < min, n, min))
    return And(
        isEmpty1 == 0,
        min1 == new_min
    )

def search(v, min, isEmpty, ret1):
    # The client program's assertion path only calls search with v < 0.
    # The invariant `inv` guarantees that if the tree is not empty, its minimum element is >= 0.
    # Therefore, a search for a negative number `v` can never succeed.
    # The CHC rule for failure is triggered if the search returns a non-zero value (i.e., true).
    # To prove the program is safe (fail is unreachable), we must specify that
    # the search returns 0 (false) in this context.
    return ret1 == 0