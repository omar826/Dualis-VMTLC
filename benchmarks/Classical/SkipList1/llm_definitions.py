# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
def inv1(i, N, isPresent, min, max, len):
	MIN = -129
	MAX = 128
	i_bounds = And(i >= 0, i <= N)
	len_is_i = (len == i)
	is_present_logic = (isPresent == If(i == 0, 0, 1))
	min_logic = (min == If(i == 0, MAX, 0))
	max_logic = (max == If(i == 0, MIN, i - 1))
	return And(i_bounds, len_is_i, is_present_logic, min_logic, max_logic)

def insert(v, isPresent, min, max, len, isPresent1, min1, max1, len1):
    op_adds = And(
        len1 == len + 1,
        isPresent1 == 1,
        min1 == If(len == 0, v, If(v < min, v, min)),
        max1 == If(len == 0, v, If(v > max, v, max))
    )
    op_no_op = And(
        len1 == len,
        min1 == min,
        max1 == max,
        isPresent1 == isPresent
    )

    must_add_cond = Or(len == 0, v < min, v > max)
    must_be_no_op_cond = And(len > 0, len == max - min + 1, v >= min, v <= max)
    can_be_either_cond = And(len > 0, len < max - min + 1, v >= min, v <= max)

    rule1 = Implies(must_add_cond, op_adds)
    rule2 = Implies(must_be_no_op_cond, op_no_op)
    rule3 = Implies(can_be_either_cond, Or(op_adds, op_no_op))

    return And(rule1, rule2, rule3)

def remove(k, min, max, len, min1, max1, len1, ret1):
    MIN = -129
    MAX = 128
    
    precond = And(len > 0, k >= min, k <= max)
    dense = (len == max - min + 1)

    op_succeeds = And(
        len1 == len - 1,
        ret1 == k,
        If(len == 1,
           And(min1 == MAX, max1 == MIN),
           # len > 1 case
           If(k == min,
              # k is the minimum
              And(max1 == max,
                  If(dense, min1 == min + 1, And(min1 > min, min1 <= max))),
              # k is not the minimum
              If(k == max,
                 # k is the maximum
                 And(min1 == min,
                     If(dense, max1 == max - 1, And(max1 < max, max1 >= min))),
                 # k is an internal point
                 And(min1 == min, max1 == max)
              )
           )
        )
    )
    
    op_fails = And(len1 == len, min1 == min, max1 == max)

    rule1 = Implies(Not(precond), op_fails)
    rule2 = Implies(And(precond, dense), op_succeeds)
    rule3 = Implies(And(precond, Not(dense)), Or(op_succeeds, op_fails))
    
    return And(rule1, rule2, rule3)