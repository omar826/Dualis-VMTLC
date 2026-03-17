# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
def inv1(i, N, isHeap, min, max, len):
	MAX = 128
	MIN = -129
	n_prop = (N > 0)
	i_range = And(0 <= i, i <= N)
	heap_prop = (isHeap == 1)
	len_prop = (len == i)
	min_prop = If(i > 0, min == 0, min == MAX)
	max_prop = If(i > 0, max == 0, max == MIN)
	return And(n_prop, i_range, heap_prop, len_prop, min_prop, max_prop)

def inv2(d, N, min, max, len, isHeap, ret):
	MAX = 128
	n_prop = (N > 0)
	count_prop = (d + len == N)
	d_range = And(0 <= d, d <= N)
	heap_prop = (isHeap == 1)
	min_max_prop = If(len > 0,
					  And(min == d, max == d),
					  And(min == MAX, max == MAX))
	ret_prop = If(d > 0, ret == d - 1, ret == MAX)
	return And(n_prop, count_prop, d_range, heap_prop, min_max_prop, ret_prop)

def insert(i, isHeap, min, max, len, isHeap1, min1, max1, len1):
	isHeap_trans = (isHeap1 == 1)
	len_trans = (len1 == len + 1)
	min_trans = If(len == 0, min1 == i, min1 == min)
	max_trans = If(len == 0, max1 == i, max1 == max)
	return And(isHeap_trans, len_trans, min_trans, max_trans)

def deleteMin(min, max, len, isHeap, min1, max1, len1, ret1, isHeap1):
	MAX = 128
	len_trans = (len1 == len - 1)
	ret_trans = (ret1 == min)
	next_val = If(len1 > 0, min + 1, MAX)
	min_trans = (min1 == next_val)
	max_trans = (max1 == next_val)
	return And(len_trans, ret_trans, min_trans, max_trans)

def downHeap(isHeap2):
	return isHeap2 == 1

def fail():
	return False