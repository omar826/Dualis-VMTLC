# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
from z3 import *

def emplace(k, v, countko, len, countko1, len1):
  """
  Defines the behavior of the 'emplace' operation.
  - If k is 1, it represents a successful insertion, incrementing both countko and len.
  - Otherwise, it's a no-op, and the state variables remain unchanged.
  This models a general-purpose insertion function where a specific key (1)
  indicates success.
  """
  return If(k == 1,
            And(countko1 == countko + 1, len1 == len + 1),
            And(countko1 == countko, len1 == len))

def inv1(i, N, countko, len):
  """
  Defines the loop invariant for the client program.
  - It establishes that the loop counter 'i', the successful operation count 'countko',
    and the length 'len' are always equal.
  - It also constrains the loop counter 'i' to be within the valid range [0, N].
  This invariant is strong enough to prove that after N iterations (i.e., when i=N),
  the count of successful operations 'countko' will also be N.
  """
  return And(i >= 0, i <= N, i == countko, i == len)