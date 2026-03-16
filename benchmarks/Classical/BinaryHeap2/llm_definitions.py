# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
from z3 import *

# Do not re-define these. They are assumed to be globally available
# in the testing environment.
#
# N, i, i1, isHeap, isHeap1, isHeap2, len_var, len1, ret1 = Ints('N i i1 isHeap isHeap1 isHeap2 len len1 ret1')

def insert(i, isHeap, len_var, isHeap1, len1):
    """
    Spec for inserting an element into a heap.
    - The length increases by 1.
    - The heap property is maintained. If it was a heap before, it is after.
    """
    return And(len1 == len_var + 1, isHeap1 == isHeap)

def deleteMin(len_var, isHeap, len1, ret1, isHeap1):
    """
    Spec for the first part of deleting the minimum element from a heap.
    - This models removing the root and replacing it with the last element.
    - The length decreases by 1.
    - This operation breaks the heap property, so isHeap1 becomes 0 (false).
    - This spec assumes it's only called on a non-empty, valid heap.
    """
    # The return value 'ret1' is unconstrained as it's not used for the proof.
    return And(len1 == len_var - 1, isHeap1 == 0)

def downheap(isHeap2):
    """
    Spec for the downheap operation.
    - Its purpose is to restore the heap property.
    - Therefore, the result isHeap2 must be 1 (true).
    """
    return isHeap2 == 1

def inv1(i, N, isHeap, len_var):
    """
    Loop invariant for the heap construction loop.
    - i: loop counter
    - N: loop bound
    - isHeap: boolean flag (1/0) for heap property
    - len_var: number of elements in the heap
    The invariant states that:
    1. The number of elements in the heap is equal to the loop counter.
    2. The structure always maintains the heap property.
    3. The loop counter is within its bounds [0, N].
    """
    return And(len_var == i, isHeap == 1, i <= N)