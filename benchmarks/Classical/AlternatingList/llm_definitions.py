# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
def inv(val, top, len, flag):
    return Or(len == 0, And(Implies(flag == 0, top == 1), Implies(flag == 1, top == 2)))

def push(val, top, len, top1, len1):
    return If(Or(val == 1, val == 2),
              And(top1 == val, len1 == len + 1),
              And(top1 == top, len1 == len))