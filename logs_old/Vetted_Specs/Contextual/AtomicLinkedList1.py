# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
from z3 import *

def insertHead(k, len, len1):
    """
    Defines the behavior of inserting an element at the head.
    The new length 'len1' is one more than the old length 'len'.
    """
    return len1 == len + 1

def popHead(len, ret1, len1):
    """
    Defines the behavior of popping an element from the head.
    The new length 'len1' is one less than the old length 'len'.
    The returned value 'ret1' is unconstrained as it's not relevant to the proof.
    """
    return len1 == len - 1

def inv1(k, N, len):
    """
    Invariant for the first loop (insertion).
    - The number of items 'len' is equal to the loop counter 'k'.
    - The loop counter 'k' is always between 0 and N (inclusive).
    """
    return And(len == k, k >= 0, k <= N)

def inv2(len, items_processed, N):
    """
    Invariant for the second loop (processing).
    - The sum of items remaining in the list 'len' and items already processed
      'items_processed' is always equal to the initial total 'N'.
    - The length 'len' is always non-negative.
    """
    return And(len + items_processed == N, len >= 0)