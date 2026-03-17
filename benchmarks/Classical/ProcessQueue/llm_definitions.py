# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
def inv(nexttime, len, min_ttw):
  return And(nexttime >= 1,
             len >= 0,
             min_ttw >= 1)

def insert(nexttime, len, len1, min_ttw, min_ttw1):
  return And(len1 == len + 1,
             min_ttw1 == If(nexttime < min_ttw, nexttime, min_ttw))

def choosenext(len, len1, min_ttw, min_ttw1):
  INT_MAX = 128
  return And(len > 0,
             len1 == len - 1,
             If(len1 == 0,
                min_ttw1 == INT_MAX,
                And(min_ttw1 >= min_ttw, min_ttw1 < INT_MAX)))