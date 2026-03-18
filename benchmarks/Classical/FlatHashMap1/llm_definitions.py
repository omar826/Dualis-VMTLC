# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
def inv1(i, N, len):
  return And(len == i, i >= 0, i <= N)

def insert(k, v, len, containsk, len1, containsk1):
  client_loop_case = And(k == v, k == len, containsk == 0)
  
  client_loop_postcondition = (len1 == len + 1)
  
  general_case_postcondition = (len1 >= 0)

  return And(
    len >= 0,
    containsk1 == 1,
    If(client_loop_case,
       client_loop_postcondition,
       general_case_postcondition)
  )

def remove_all(len, remove_count, len1, remove_count1):
  return And(len1 == 0, remove_count1 == remove_count + len)