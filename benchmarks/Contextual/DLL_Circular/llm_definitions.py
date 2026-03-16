# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
from z3 import *

def inv(val_param, max_val_param):
    """
    Defines the loop invariant for the client program.
    It must hold at the beginning of the loop and be preserved by each iteration.
    Based on the analysis:
    1. `val` starts at 0 and is capped at 3. So, `0 <= val_param <= 3`.
    2. `max` tracks the maximum value `val` has ever held. So, `val_param <= max_val_param`.
    3. From (1) and (2), `max_val_param` must also be between 0 and 3.
    4. The assertion in the CHCs (rule 5) requires that the invariant implies `0 <= max_val_param <= 3`.
    The simplest non-redundant form is `0 <= val <= max <= 3`.
    """
    return And(0 <= val_param, val_param <= max_val_param, max_val_param <= 3)

def push(val_in, max_in, max_out):
    """
    Defines the state transition for the `max` variable.
    The `max` variable is intended to store the maximum value that `val` has reached.
    Therefore, the new `max` (`max_out`) should be the greater of the old `max` (`max_in`)
    and the current `val` (`val_in`).
    """
    return max_out == If(val_in > max_in, val_in, max_in)