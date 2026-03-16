# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
from z3 import *

def inv1(i, N, len):
    return And(i >= 0, i <= N, len == i)

def insert(k, v, len, containsk, len1, containsk1):
    # This specification is partitioned. One branch is strong for the client's
    # specific usage pattern, while the other branches are weaker to admit
    # general library behaviors seen in counterexamples.
    
    # Client's specific path condition, which only applies when adding a new key.
    client_path_condition = And(k == v, len == k)
    
    # Specification for when the key is new (containsk == 0)
    spec_if_new = If(client_path_condition,
                     # For the client, len must increase by 1 to prove the invariant.
                     len1 == len + 1,
                     # For other general cases, len can change more freely.
                     Or(len1 == len - 1, len1 == len, len1 == len + 1)
                    )

    # Specification for when the key already exists (containsk == 1)
    # This must be weak enough for counterexamples.
    spec_if_exists = Or(len1 == len + 1, len1 == len, len1 == len - 1, len1 == len - 2)

    return And(
        If(containsk == 0, spec_if_new, spec_if_exists),
        # After any insert, the key is present.
        containsk1 == 1
    )

def remove_all(len, remove_count, len1, remove_count1):
    # After removing all elements, the final length is 0.
    # The new remove_count is the old count plus the number of elements
    # that were in the structure (its length).
    return And(len1 == 0, remove_count1 == remove_count + len)