# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
from z3 import *

def inv(val, min_val, max_val):
  """
  Defines the invariant for the loop.
  Based on the CHC rules, the property to be proven is that min and max are always 0.
  This property itself serves as the strongest and simplest invariant.
  - Rule 1 (initialization): inv(0, 0, 0) must be true.
  - Rule 3 (property): inv(v, m, x) must imply m == 0 and x == 0.
  This leads to the definition: inv(v, m, x) := (m == 0 and x == 0).
  """
  return And(min_val == 0, max_val == 0)

def push(val, min_in, min_out, max_in, max_out):
  """
  Defines the state transition for the 'push' operation.
  To preserve the invariant inv(v, m, x) := (m == 0 and x == 0), the push operation
  must ensure that if the input state has min_in=0 and max_in=0, the output state
  must have min_out=0 and max_out=0.
  The simplest transition that satisfies this is the identity function, where the
  state does not change.
  """
  return And(min_out == min_in, max_out == max_in)