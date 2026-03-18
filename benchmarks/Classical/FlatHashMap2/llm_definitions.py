# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
from z3 import *

def inv1(i, N, len):
    return And(i >= 0, i <= N, len == i)

def insert(k, v, len, containsk, len1, containsk1):
    # This specification states that an insert operation always increases
    # the length by 1 and results in the key being present (containsk1 = 1).
    # This is a valid and general specification for an "add" or "append"
    # operation where new, unique elements are added.
    return And(len1 == len + 1, containsk1 == 1)

def remove_none(len, remove_count, len1, remove_count1):
    # This specification states that the function is a no-op.
    # The length and the count of removed items remain unchanged.
    return And(len1 == len, remove_count1 == remove_count)