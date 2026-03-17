# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
def inv1(i, N, len, containsk):
    cond_N = (N > 0)
    cond_bounds = And(0 <= i, i <= N)
    cond_len = (len == i)
    cond_containsk = If(i == 0, containsk == 0, containsk == 1)
    return And(cond_N, cond_bounds, cond_len, cond_containsk)

def inv2(i, N, len, containsk, flag, ret):
    cond_N = (N > 0)
    cond_bounds = And(0 <= i, i <= N)
    cond_containsk = (containsk == 1)
    cond_flag = (flag == 1 - (i % 2))

    # Case N > 1
    # For N>1, an erase attempt is always on a list with len > 1, so it always succeeds.
    num_erased = (i + 1 - flag) / 2
    inv_N_gt_1_len = (len == N - num_erased)
    # ret holds the value of k from the last successful erase, which is the last even index <= i-1.
    inv_N_gt_1_ret = If(i > 0, ret == (i - 1) - ((i - 1) % 2), True)
    inv_N_gt_1 = And(inv_N_gt_1_len, inv_N_gt_1_ret)

    # Case N = 1
    # len is always 1. erase is a no-op at i=0. ret must become 0 for post-condition.
    inv_N1_len = (len == 1)
    inv_N1_ret = If(i > 0, ret == 0, True) # After i=0, ret must be 0
    inv_N1 = And(inv_N1_len, inv_N1_ret)

    return And(cond_N, cond_bounds, cond_containsk, cond_flag, If(N > 1, inv_N_gt_1, inv_N1))

def insert(k, value, len, containsk, len1, containsk1):
    return And(len1 == len + 1, containsk1 == 1)

def erase(k, len, flag, len1, ret1):
    # This function is only called when flag=1 in the program.
    # The erase operation succeeds only if len > 1.
    erase_op = And(len1 == len - 1, ret1 == k)
    # If len <= 1, it's a no-op on len.
    # For the program to be correct for N=1, ret must become 0.
    # This happens when i=0, so k=0. Setting ret1=k handles this.
    noop_op = And(len1 == len, ret1 == k)
    return If(len > 1, erase_op, noop_op)