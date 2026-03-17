# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
def insert(k, v, len, containsk, len1, containsk1):
    return And(
        If(containsk == 0, len1 == len + 1, len1 == len),
        containsk1 == 1
    )

def erase(k, len, flag, len1, ret1):
    return And(len1 == len - 1, ret1 == k)

def inv1(i, N, len):
    return And(N > 0, i >= 0, i <= N, len == i)

def inv2(i, N, len, flag, ret):
    n_cond = N > 0
    bounds_cond = And(i >= 0, i <= N)
    flag_parity_cond = If(i % 2 == 0, flag == 1, flag == 0)
    
    num_erased = If(flag == 1, i / 2, (i + 1) / 2)
    len_cond = (len == N - num_erased)
    
    ret_cond = If(i == 0,
                  ret == 128,
                  If(flag == 0,
                     ret == i - 1,
                     ret == i - 2
                  )
                 )
    return And(n_cond, bounds_cond, flag_parity_cond, len_cond, ret_cond)

def fail():
    return False

def downHeap(a, b, c, d, e):
    return True