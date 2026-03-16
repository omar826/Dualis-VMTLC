# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
def generateTokens(b_size, avai_tokens):
  return avai_tokens == b_size

def consume(c_rate, avai_tokens, avai_tokens1):
  return avai_tokens1 == avai_tokens - c_rate

def inv1(avai_tokens, b_size, c_rate, consumed_tokens):
    # The invariant captures two possible macro-states of the loop, plus static preconditions.
    # 1. The initial state before any consumption.
    initial_state = And(consumed_tokens == 0, avai_tokens == b_size)
    
    # 2. The state after at least one consumption has occurred.
    # In this state, consumed_tokens must be at least c_rate, and the token conservation law holds.
    loop_state = And(consumed_tokens >= c_rate, avai_tokens + consumed_tokens == b_size)
    
    # The invariant is that the system is always in one of these two states,
    # and the static preconditions hold. This form avoids the computationally
    # expensive modulo operator which likely caused the timeout, while being
    # strong enough to prove the assertion.
    return And(
        b_size >= c_rate,
        c_rate > 0,
        Or(initial_state, loop_state)
    )