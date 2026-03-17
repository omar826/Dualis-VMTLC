# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
def inv(len, minDiff):
    return And(len >= 0, minDiff >= 0)

def addStockOrder(len, len1, stock, order, minDiff, minDiff1):
    # This function's parameters are mapped positionally from the CHC rule:
    # CHC rule call: (addStockOrder stock order len minDiff len1 minDiff1)
    # Python signature: def addStockOrder(len, len1, stock, order, minDiff, minDiff1)
    #
    # Positional Mapping:
    # py_len      -> chc_stock
    # py_len1     -> chc_order
    # py_stock    -> chc_len
    # py_order    -> chc_minDiff
    # py_minDiff  -> chc_len1
    # py_minDiff1 -> chc_minDiff1
    #
    # Abstract program logic (in CHC terms):
    # 1. chc_len1 = chc_len + 1
    # 2. chc_minDiff1 = min(chc_minDiff, chc_stock - chc_order)
    #
    # Translated logic using Python parameter names:
    # 1. py_minDiff = py_stock + 1
    # 2. py_minDiff1 = min(py_order, py_len - py_len1)

    len_update = (minDiff == stock + 1)
    
    new_diff = len - len1
    min_diff_update = (minDiff1 == If(new_diff < order, new_diff, order))
    
    return And(len_update, min_diff_update)