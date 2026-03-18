# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
from z3 import *

def inv1(i, N, countko, countkt, len):
    """
    Loop invariant for the client program.
    - i: loop counter
    - N: loop bound
    - countko: count of key '1'
    - countkt: count of key '2'
    - len: total number of elements
    """
    # The loop runs from i = 0 to N.
    # In each iteration, we insert key '1'.
    # So, after i iterations:
    # - The counter i is between 0 and N.
    # - The count of key '1' (countko) is exactly i.
    # - The count of key '2' (countkt) is 0, as it's only inserted after the loop.
    # - The total length (len) is also i.
    return And(i >= 0, i <= N, countko == i, countkt == 0, len == i)

def emplace(k, v, countko, countkt, len, countko1, countkt1, len1):
    """
    Specification for a general-purpose emplace/insert function.
    - k, v: key-value pair to insert
    - countko, countkt, len: state before insertion
    - countko1, countkt1, len1: state after insertion
    """
    # This function models an insertion operation that specifically tracks
    # the counts of keys 1 and 2.
    
    # The total length always increases by 1 after any insertion.
    len_update = (len1 == len + 1)
    
    # The counts of keys 1 and 2 are updated based on the key 'k' being inserted.
    # If k is 1, countko is incremented.
    # If k is 2, countkt is incremented.
    # For any other key, neither special counter is changed.
    count_update = If(k == 1,
                      And(countko1 == countko + 1, countkt1 == countkt),
                      If(k == 2,
                         And(countko1 == countko, countkt1 == countkt + 1),
                         And(countko1 == countko, countkt1 == countkt)))
                         
    return And(len_update, count_update)