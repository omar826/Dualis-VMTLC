# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
def inv(pmin, pisEmpty, pn):
    return Implies(Not(pisEmpty), pmin >= 0)

def insert(pn, pmin, pmin1, pisEmpty, pisEmpty1):
    post_cond = And(
        pisEmpty1 == False,
        pmin1 == If(pisEmpty, pn, If(pn < pmin, pn, pmin))
    )
    return Implies(pn >= 0, post_cond)

def search(pv, pmin, pisEmpty, pret1):
    return And(
        Implies(pisEmpty, Not(pret1)),
        Implies(pret1, pv >= pmin)
    )