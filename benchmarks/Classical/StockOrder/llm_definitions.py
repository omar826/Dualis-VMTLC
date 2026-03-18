# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
def inv(len, minDiff):
  return And(len >= 0, minDiff >= 0)

def addStockOrder(len, len1, stock, order, minDiff, minDiff1):
  # Based on the CHC rule (addStockOrder stock order len minDiff len1 minDiff1),
  # arguments are mapped positionally to this Python function's signature.
  # The client's precondition `order <= stock` is therefore mapped to `len1 <= len`.

  client_precondition = (len1 <= len)

  # The state update logic that is required to prove the client's invariant.
  # This logic is derived from the abstract program's behavior, translated
  # through the positional mapping.
  # Abstract: len' = len + 1
  # Translated: chc.len1 = chc.len + 1  =>  py.minDiff = py.stock + 1
  len_update = (minDiff == stock + 1)

  # Abstract: minDiff' = min(minDiff, stock - order)
  # Translated: chc.minDiff1 = min(chc.minDiff, chc.stock - chc.order)
  #          => py.minDiff1 = min(py.order, py.len - py.len1)
  min_diff_update = (minDiff1 == If(len - len1 < order, len - len1, order))

  client_behavior = And(len_update, min_diff_update)

  # The specification for the general function only needs to enforce the client's
  # behavior when the client's preconditions are met. For all other inputs
  # (like those in the failing test cases where stock < order => len < len1),
  # the function can be permissive (return True).
  return Implies(client_precondition, client_behavior)