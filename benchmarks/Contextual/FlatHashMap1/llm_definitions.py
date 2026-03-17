# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
from z3 import *

# This is a dummy Z3 script that can be used to check the validity of the generated functions
# It is not part of the required output.
# from z3 import *
#
# # Z3 variables
# N, i, i1, containsk, containsk1, len, len1, remove_count, remove_count1, k, v = Ints('N i i1 containsk containsk1 len len1 remove_count remove_count1 k v')
# fail = Bool('fail')
#
# # Helper function from CHC
# def is_valid(x):
#     return Or(x == 1, x == 0)

def inv1(i, N, len, containsk):
    is_non_empty = If(i > 0, 1, 0)
    return And(i >= 0, i <= N, len == i, containsk == is_non_empty)

def insert(k, v, len, containsk, len1, containsk1):
    return And(len1 == len + 1, containsk1 == 1)

def remove_all(len, remove_count, len1, remove_count1):
    return And(len1 == 0, remove_count1 == remove_count + len)

# # Z3 Solver
# s = Solver()
#
# # Rule 1: Base case
# s.add(Not(Implies(And(N > 0, i == 0, containsk == 0, len == 0), inv1(i, N, len, containsk))))
#
# # Rule 2: Inductive step
# s.add(Not(Implies(And(inv1(i, N, len, containsk), is_valid(containsk), i < N, k == i, v == i, insert(k, v, len, containsk, len1, containsk1), i1 == i + 1), inv1(i1, N, len1, containsk1))))
#
# # Rule 3: Post-condition
# s.add(Not(Implies(And(inv1(i, N, len, containsk), is_valid(containsk), Not(i < N), remove_count == 0, remove_all(len, remove_count, len1, remove_count1), Not(And(remove_count1 == N, len1 == 0))), fail)))
#
# # Check for counterexamples
# print("Checking rule 1...")
# if s.check() == sat:
#     print("Counterexample for rule 1 found:")
#     print(s.model())
# else:
#     print("Rule 1 is valid.")
#
# s.reset()
#
# print("\nChecking rule 2...")
# s.add(Not(Implies(And(inv1(i, N, len, containsk), is_valid(containsk), i < N, k == i, v == i, insert(k, v, len, containsk, len1, containsk1), i1 == i + 1), inv1(i1, N, len1, containsk1))))
# if s.check() == sat:
#     print("Counterexample for rule 2 found:")
#     print(s.model())
# else:
#     print("Rule 2 is valid.")
#
# s.reset()
#
# print("\nChecking rule 3...")
# s.add(Not(Implies(And(inv1(i, N, len, containsk), is_valid(containsk), Not(i < N), remove_count == 0, remove_all(len, remove_count, len1, remove_count1), Not(And(remove_count1 == N, len1 == 0))), fail)))
# if s.check() == sat:
#     print("Counterexample for rule 3 found:")
#     print(s.model())
# else:
#     print("Rule 3 is valid.")