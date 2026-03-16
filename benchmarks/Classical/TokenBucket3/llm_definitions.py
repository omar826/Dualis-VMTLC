# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
def generateTokens(b_size, avai_tokens):
    """
    Specifies that the initial number of available tokens is equal to the bucket size.
    """
    return avai_tokens == b_size

def consume(c_rate, avai_tokens, avai_tokens1):
    """
    Specifies the state change of consuming tokens: the new token count is the old count
    minus the consumption rate.
    """
    return avai_tokens1 == avai_tokens - c_rate

def inv1(avai_tokens, b_size, c_rate, consumed_tokens):
    """
    Loop invariant for the token bucket algorithm. It states that:
    1. The sum of available tokens and consumed tokens is always equal to the total bucket size.
    2. The number of available tokens is always non-negative.
    """
    return And(avai_tokens + consumed_tokens == b_size, avai_tokens >= 0)