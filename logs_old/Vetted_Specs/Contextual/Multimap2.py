# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
from z3 import *

def inv1(i, N, countko, countkt, len):
    # This invariant captures the state at the beginning of each loop iteration.
    # i: loop counter, from 0 to N.
    # countko: Number of times key '1' was emplaced, which equals i.
    # len: Total number of emplacements, which also equals i.
    # countkt: Number of times key '2' was emplaced, which is 0 inside the loop.
    return And(i >= 0, i <= N, countko == i, len == i, countkt == 0)

def emplace(k, v, countko, countkt, len, countko1, countkt1, len1):
    # This relation models the emplace operation inside the loop.
    # In the context of the calling rule, k is always 1.
    # Therefore, countko (count-key-one) is incremented.
    # The total length is also incremented.
    # countkt (count-key-two) remains unchanged.
    return And(countko1 == countko + 1,
               countkt1 == countkt,
               len1 == len + 1)

def emplace1(k, v, countko, countkt, len, countko1, countkt1, len1):
    # This relation models the emplace operation after the loop.
    # In the context of the calling rule, k is always 2.
    # Therefore, countkt (count-key-two) is incremented.
    # The total length is also incremented.
    # countko (count-key-one) remains unchanged.
    return And(countko1 == countko,
               countkt1 == countkt + 1,
               len1 == len + 1)