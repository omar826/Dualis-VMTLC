# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
def push(val, top, len, top1, len1):
    return And(top1 == val, len1 == len + 1)

def inv(top, len, flag):
    return Or(len == 0, And(Implies(flag == 0, top == 1), Implies(flag == 1, top == 2)))

def push1(val, top, len, top1, len1):
    return And(top1 == val, len1 == len + 1)