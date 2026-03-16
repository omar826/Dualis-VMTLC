# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
from z3 import *

def inv1(i, N, countko, countkt, len):
    return And(i >= 0, i <= N, countko == i, len == i, countkt == 0)

def emplace(k, v, countko, countkt, len, countko1, countkt1, len1):
    update_k1 = And(countko1 == countko + 1, countkt1 == countkt)
    update_k2 = And(countko1 == countko, countkt1 == countkt + 1)
    update_other = And(countko1 == countko, countkt1 == countkt)
    
    return And(
        len1 == len + 1,
        If(k == 1, 
           update_k1,
           If(k == 2, 
              update_k2, 
              update_other
           )
        )
    )