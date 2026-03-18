# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
def inv(min, isEmpty):
    return Or(And(isEmpty == 1, min == 128),
              And(isEmpty == 0, min >= 0))

def insert(n, min, min1, isEmpty, isEmpty1):
    empty_case = And(min1 == n, isEmpty1 == 0)
    non_empty_case = And(min1 == If(n < min, n, min), isEmpty1 == 0)
    return If(isEmpty == 1, empty_case, non_empty_case)

def search(v, min, isEmpty, ret1):
    empty_case = (ret1 == 0)
    non_empty_case = If(v < min,
                        ret1 == 0,
                        Or(ret1 == 0, ret1 == 1))
    return If(isEmpty == 1, empty_case, non_empty_case)