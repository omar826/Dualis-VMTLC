# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
def inv(nexttime, len, min_ttw):
    return And(
        nexttime == len + 1,
        len >= 0,
        Implies(len > 0, min_ttw >= 1)
    )

def insert(nexttime, len, len1, min_ttw, min_ttw1):
    len_update = (len1 == len + 1)
    min_ttw_update = (min_ttw1 == If(len == 0, nexttime, If(min_ttw < nexttime, min_ttw, nexttime)))
    return And(len_update, min_ttw_update)

def choosenext(len, len1, min_ttw, min_ttw1):
    MAX = 128
    len_update = (len1 == len - 1)
    min_ttw_update = If(len1 == 0, min_ttw1 == MAX, min_ttw1 >= min_ttw)
    return And(len_update, min_ttw_update)