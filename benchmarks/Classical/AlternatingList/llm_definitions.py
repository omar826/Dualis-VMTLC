# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
def inv(val, top, len, flag):
    property_when_non_empty = And(Implies(flag == 0, top == 1), Implies(flag == 1, top == 2))
    return And(len >= 0, Implies(len > 0, property_when_non_empty))

def push(val, top, len, top1, len1):
    is_client_val = Or(val == 1, val == 2)
    standard_push = And(top1 == val, len1 == len + 1)
    identity_op = And(top1 == top, len1 == len)
    return If(is_client_val, standard_push, identity_op)