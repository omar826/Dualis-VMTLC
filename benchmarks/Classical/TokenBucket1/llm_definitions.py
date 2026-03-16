# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
def generateTokens(b_size, avai_tokens):
    """
    Specification for generateTokens.
    Relates the bucket size (b_size) to the number of available tokens generated.
    The behavior is that the number of available tokens becomes equal to the bucket size.
    """
    return avai_tokens == b_size

def consume(c_rate, avai_tokens, avai_tokens1):
    """
    Specification for consume.
    Relates the available tokens before (avai_tokens) and after (avai_tokens1)
    consumption by a given rate (c_rate).
    The behavior is a simple subtraction.
    """
    return avai_tokens1 == avai_tokens - c_rate

def inv1(avai_tokens, b_size, c_rate, consumed_tokens):
    """
    Loop invariant for the token consumption process.
    It must hold before the loop, be preserved by each iteration, and imply
    the final assertion upon loop termination.
    Two key properties are maintained:
    1. The number of available tokens is always non-negative.
    2. The sum of available and consumed tokens is a conserved quantity,
       always equal to the initial bucket size.
    """
    return And(avai_tokens >= 0, avai_tokens + consumed_tokens == b_size)