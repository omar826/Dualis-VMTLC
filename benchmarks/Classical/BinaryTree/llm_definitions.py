# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
from z3 import *

def inv (min, isEmpty):
    MAX = 128
    return If(isEmpty == 1, min == MAX, min >= 0)

def insert(n, min, min1, isEmpty, isEmpty1):
    # After an insert, the tree is no longer empty.
    # The new minimum is the smaller of the old minimum and the new element n.
    # If the tree was empty, the new minimum is just n.
    new_min = If(isEmpty == 1, n, If(n < min, n, min))
    return And(isEmpty1 == 0, min1 == new_min)

def search(v, min, isEmpty, ret1):
    # A general search function specification.
    # If the tree is empty, the element cannot be found (ret1 == 0).
    # If the element 'v' is smaller than the minimum element in the tree, it cannot be found.
    # Otherwise, the result is undetermined by this specification (ret1 could be 0 or 1).
    # This is strong enough for the client, which searches for v < 0 while the invariant guarantees min >= 0.
    return Implies(Or(isEmpty == 1, And(isEmpty == 0, v < min)), ret1 == 0)