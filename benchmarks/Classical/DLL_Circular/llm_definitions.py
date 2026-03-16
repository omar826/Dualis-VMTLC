# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
def inv(val_param, max_val_param):
  return And(0 <= val_param, val_param <= 3, 0 <= max_val_param, max_val_param <= val_param)

def push(val_in, max_in, max_out):
  return max_out == If(val_in > max_in, val_in, max_in)