# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
def inv(len, minPrio, maxPacketSize):
    initial_state = And(len == 0, minPrio == -1, maxPacketSize == -1)
    non_empty_state = And(len > 0,
                          minPrio == 1,
                          maxPacketSize >= 1,
                          maxPacketSize <= 499)
    return Or(initial_state, non_empty_state)

def append(prio, packetSize, len, minPrio, maxPacketSize, len1, minPrio1, maxPacketSize1):
    return And(len1 == len + 1,
               minPrio1 == If(len == 0, prio, If(prio < minPrio, prio, minPrio)),
               maxPacketSize1 == If(len == 0, packetSize, If(packetSize > maxPacketSize, packetSize, maxPacketSize)))

def processQueue(len, minPrio, maxPacketSize, len1, minPrio1, maxPacketSize1):
    # The length of the queue can only decrease or stay the same.
    len_constraint = (len1 <= len)
    
    # If the queue becomes empty after processing, the stats must be reset.
    # This is required by the assertion in the client program.
    empty_constraint = Implies(len1 == 0, And(minPrio1 == -1, maxPacketSize1 == -1))
    
    # If nothing is processed (noop), the state remains identical.
    noop_constraint = Implies(len1 == len, And(minPrio1 == minPrio, maxPacketSize1 == maxPacketSize))

    # If some items are processed but the queue is not empty (0 < len1 < len),
    # the new minPrio and maxPacketSize are unconstrained, as we don't know
    # which elements were removed. This is implicitly handled by not adding
    # constraints for this case.

    return And(len_constraint, empty_constraint, noop_constraint)