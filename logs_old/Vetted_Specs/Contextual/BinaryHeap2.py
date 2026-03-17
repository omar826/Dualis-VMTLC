# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
from z3 import And, Implies, Not, Or, If

def insert(i, isHeap, len, isHeap1, len1):
    """
    Specifies the behavior of the insert operation.
    - The length of the heap increases by 1.
    - The heap property is maintained after insertion.
    """
    return And(len1 == len + 1, isHeap1 == 1)

def deleteMin(len, isHeap, len1, ret1, isHeap1):
    """
    Specifies the behavior of the deleteMin operation.
    - This is called on a valid heap with len > 0.
    - The length decreases by 1.
    - If the original heap had more than one element, deleting the root and swapping
      the last element to the top breaks the heap property (isHeap1 = 0).
    - If the original heap had exactly one element, the resulting empty heap is
      a valid heap (isHeap1 = 1).
    """
    return And(len1 == len - 1, If(len > 1, isHeap1 == 0, isHeap1 == 1))

def downheap(isHeap2):
    """
    Specifies the behavior of the downheap operation.
    - Its purpose is to restore the heap property.
    - After execution, the state variable isHeap2 is guaranteed to be true (1).
    """
    return isHeap2 == 1

def inv1(i, N, isHeap, len):
    """
    Defines the loop invariant for the insertion phase.
    - The loop counter 'i' is between 0 and N (inclusive).
    - The length of the heap 'len' is equal to the number of iterations 'i'.
    - The heap property 'isHeap' is always maintained during the insertion loop.
    """
    return And(i >= 0, i <= N, len == i, isHeap == 1)