# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
def generateTokens(b_size, avai_tokens1):
    return avai_tokens1 == b_size

def consume(c_rate, avai_tokens, avai_tokens1):
    return If(avai_tokens >= c_rate, 
              avai_tokens1 == avai_tokens - c_rate, 
              avai_tokens1 == avai_tokens)

def inv1(avai_tokens, b_size, c_rate, consumed_tokens):
    return And(
        b_size >= c_rate,
        c_rate > 0,
        avai_tokens + consumed_tokens == b_size,
        consumed_tokens >= 0,
        Or(consumed_tokens == 0, consumed_tokens >= c_rate)
    )