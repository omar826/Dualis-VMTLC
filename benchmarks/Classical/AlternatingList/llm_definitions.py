# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
def inv(val, top, len, flag):
    MAX = 10
    init_state = And(len == 0, flag == 1, top == MAX)
    odd_len_state = And(len > 0, len % 2 == 1, flag == 0, top == 1)
    even_len_state = And(len > 0, len % 2 == 0, flag == 1, top == 2)
    return Or(init_state, odd_len_state, even_len_state)

def push(val, top, len, top1, len1):
    push_succeeds = And(top1 == val, len1 == len + 1)
    push_noop = And(top1 == top, len1 == len)
    return If(Or(val == 1, val == 2),
              push_succeeds,
              Or(push_succeeds, push_noop))