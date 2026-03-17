# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
from z3 import *

def inv1(i, N, len, containsk):
  """
  Loop invariant for the main loop.
  - i: loop counter
  - N: loop bound
  - len: current length of the data structure
  - containsk: flag indicating if a key 'k' is present
  The invariant states that the length is always equal to the loop counter,
  and the loop counter is within the bounds [0, N].
  """
  return And(i <= N, len == i)

def insert(k, v, len, containsk, len1, containsk1):
  """
  Specification for the 'insert' operation.
  - k, v: key and value to insert
  - len, containsk: state before insertion
  - len1, containsk1: state after insertion
  The operation increases the length by 1.
  It also sets the 'containsk' flag to true (1), as an element is now present.
  """
  return And(len1 == len + 1, containsk1 == 1)

def remove_none(len, remove_count, len1, remove_count1):
  """
  Specification for the 'remove_none' operation.
  - len, remove_count: state before the operation
  - len1, remove_count1: state after the operation
  This operation does not change the state. The length and remove_count remain the same.
  """
  return And(len1 == len, remove_count1 == remove_count)