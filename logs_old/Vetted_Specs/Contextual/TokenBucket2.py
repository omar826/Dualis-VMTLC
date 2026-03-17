# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
def generateTokens(b_size, avai_tokens):
    return avai_tokens == b_size

def consume(c_rate, avai_tokens, avai_tokens1):
    return avai_tokens1 == avai_tokens - c_rate

def inv1(avai_tokens, b_size, c_rate, consumed_tokens):
    # Invariant must capture static assumptions from initialization
    static_assumptions = And(b_size > 0, c_rate > 0, b_size >= c_rate)
    
    # Invariant must capture the relationship between variables
    token_conservation = (avai_tokens + consumed_tokens == b_size)
    
    # Invariant on the state of consumed_tokens
    # It starts at 0 and is always incremented by c_rate, so it's a non-negative multiple of c_rate
    consumed_properties = And(consumed_tokens >= 0, consumed_tokens % c_rate == 0)

    return And(static_assumptions, token_conservation, consumed_properties)