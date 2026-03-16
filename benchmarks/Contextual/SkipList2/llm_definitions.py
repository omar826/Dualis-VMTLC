# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
from z3 import *

def inv1(i, N, isPresent, min, max, len):
  """
  Loop invariant for the main loop.
  It captures the state of the data structure after 'i' elements (0, 1, ..., i-1) have been inserted.
  - When i=0 (initial state), the set is empty, represented by special min/max values.
  - When i>0, the set contains {0, ..., i-1}, so min is 0, max is i-1, and len is i.
  """
  initial_state = And(isPresent == 0, min == 128, max == -129)
  loop_state = And(isPresent == 1, min == 0, max == i - 1)
  
  return And(
    i >= 0,
    i <= N,
    len == i,
    If(i == 0, initial_state, loop_state)
  )

def insert(v, isPresent, min, max, len, isPresent1, min1, max1, len1):
  """
  Relational specification for the 'insert' operation.
  It defines the next state (isPresent1, min1, max1, len1) based on the current state
  and the value 'v' being inserted.
  - The length is always incremented.
  - The set is marked as present (not empty).
  - min and max are updated by comparing with the new value 'v'.
    The initial state values (min=MAX, max=MIN) ensure this works for the first element.
  """
  return And(
    isPresent1 == 1,
    min1 == If(v < min, v, min),
    max1 == If(v > max, v, max),
    len1 == len + 1
  )

def lower_bound(k, lb_ret1):
  """
  Relational specification for the 'lower_bound' function.
  The client program asserts that the return value is >= k.
  This specification defines the function's behavior to satisfy this property, which is
  the fundamental definition of a lower bound. Making this the specification
  is the most direct way to satisfy the verification goal.
  """
  return lb_ret1 >= k