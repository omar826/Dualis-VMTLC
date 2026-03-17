# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
def generateTokens(b_size, avai_tokens):
  return avai_tokens == b_size

def consume(c_rate, avai_tokens, avai_tokens1):
  return avai_tokens1 == avai_tokens - c_rate

def inv1(avai_tokens, b_size, c_rate, consumed_tokens):
  return And(
      avai_tokens + consumed_tokens == b_size,
      avai_tokens >= 0,
      consumed_tokens >= 0,
      c_rate > 0
  )