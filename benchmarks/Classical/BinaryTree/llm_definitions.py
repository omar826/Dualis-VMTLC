# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
def inv(min, isEmpty):
    MAX = 128
    return If(isEmpty == 1,
              min == MAX,
              If(isEmpty == 0,
                 min >= 0,
                 False))

def insert(n, min, min1, isEmpty, isEmpty1):
    post_is_empty = (isEmpty1 == 0)
    post_min = (min1 == If(n < min, n, min))
    return And(post_is_empty, post_min)

def search(v, min, isEmpty, ret1):
    must_fail = Or(isEmpty == 1, v < min)
    return If(must_fail, ret1 == 0, True)