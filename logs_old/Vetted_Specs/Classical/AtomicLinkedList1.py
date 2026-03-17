# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
from z3 import *

def insertHead(k, len, len1):
  """
  Specifies the behavior of inserting an element at the head.
  The new length (len1) is the old length (len) plus one.
  """
  return len1 == len + 1

def popHead(len, ret1, len1):
  """
  Specifies the behavior of popping an element from the head.
  This is only valid if the list is not empty (len > 0).
  The new length (len1) is the old length (len) minus one.
  The returned value (ret1) is unconstrained.
  """
  return And(len > 0, len1 == len - 1)

def inv1(k, N, len):
  """
  Invariant for the first loop.
  - k is the loop counter, from 0 to N.
  - len is the length of the list.
  The invariant states that the length of the list is equal to the number of iterations completed.
  """
  return And(k >= 0, k <= N, len == k)

def inv2(len, items_processed, N):
  """
  Invariant for the second loop.
  - len is the number of items remaining in the list.
  - items_processed is the number of items popped.
  - N is the total number of items initially.
  The invariant states that the sum of items remaining and items processed is always equal to the initial total.
  """
  return And(len >= 0, items_processed >= 0, len + items_processed == N)