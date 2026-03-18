# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
def insert(k, v, len, min, max, len1, min1, max1):
  MAX = 128
  MIN = -129
  
  insert_case = And(
      len1 == len + 1,
      min1 == If(len == 0, k, If(k < min, k, min)),
      max1 == If(len == 0, k, If(k > max, k, max))
  )
  
  update_case = And(
      len1 == len,
      min1 == min,
      max1 == max
  )
  
  # If the collection is empty, it must be an insert.
  if_empty = insert_case
  
  # If non-empty:
  # If k is outside the current range, it must be a new insert.
  # If k is on a boundary (min or max), it's an update.
  # If k is inside the range, it could be an insert (filling a gap) or an update.
  if_non_empty = If(Or(k < min, k > max), 
                    insert_case,
                    If(Or(k == min, k == max),
                       update_case,
                       Or(insert_case, update_case)))

  return If(len == 0, if_empty, if_non_empty)

def find(k, len, min, max, ret1):
  MIN = -129
  return Implies(And(len > 0, min <= k, k <= max), ret1 != MIN)

def inv1(i, N, len, min, max):
  MAX = 128
  MIN = -129
  
  i_range_cond = And(0 <= i, i <= N)
  
  len_cond = (len == i)
  
  init_min_max_cond = And(min == MAX, max == MIN)
  
  loop_min_max_cond = And(min == 0, max == i - 1)
  
  min_max_cond = If(i == 0, init_min_max_cond, loop_min_max_cond)
  
  return And(i_range_cond, len_cond, min_max_cond)