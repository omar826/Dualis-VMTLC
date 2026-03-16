# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
from z3 import *

def inv (min, isEmpty):
    MAX = 128
    return If(isEmpty == 1, min == MAX, min >= 0)

def insert(n, min, min1, isEmpty, isEmpty1):
    return And(isEmpty1 == 0, min1 == If(n < min, n, min))

def search(v, min, isEmpty, ret1):
    # If the tree is empty or the value 'v' is less than the minimum element,
    # 'v' cannot be in the tree, so the search must return false (ret1 == 0).
    # Otherwise, the result is inconclusive from the perspective of 'min' and 'isEmpty' alone.
    return Implies(Or(isEmpty == 1, v < min), ret1 == 0)