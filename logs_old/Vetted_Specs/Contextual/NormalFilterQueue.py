# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
def inv(len, maxPrio, minPacketSize):
    # Invariant for the loop state.
    # len must be non-negative.
    # If the queue is empty (len == 0), maxPrio and minPacketSize have initial sentinel values.
    # If the queue is not empty (len > 0), all appended packets have prio=0 and size>=500.
    # Thus, maxPrio must be 0, and minPacketSize must be at least 500.
    is_empty = (len == 0)
    empty_state = And(maxPrio == -1, minPacketSize == -1)
    non_empty_state = And(maxPrio == 0, minPacketSize >= 500)
    
    return And(
        len >= 0,
        If(is_empty, empty_state, non_empty_state)
    )

def append(prio, packetSize, len, maxPrio, minPacketSize, len1, maxPrio1, minPacketSize1):
    # Defines the state transition for appending a packet.
    # The new length is incremented.
    len_update = (len1 == len + 1)
    
    # The new maxPrio is the max of the old one and the new packet's priority.
    maxPrio_update = (maxPrio1 == If(prio > maxPrio, prio, maxPrio))
    
    # The new minPacketSize is the size of the new packet if it's the first one added,
    # otherwise it's the minimum of the old minPacketSize and the new packet's size.
    minPacketSize_update = (minPacketSize1 == If(len == 0,
                                                 packetSize,
                                                 If(packetSize < minPacketSize, packetSize, minPacketSize)))
                                                 
    return And(len_update, maxPrio_update, minPacketSize_update)

def processQueue(len, maxPrio, minPacketSize, len1, maxPrio1, minPacketSize1):
    # The specification for this function is constrained by two facts:
    # 1. The abstract program asserts: len1 == 0 ==> (maxPrio1 == maxPrio && minPacketSize1 == minPacketSize)
    # 2. The CHC fail rule implies: len1 == 0 ==> (maxPrio1 == -1 && minPacketSize1 == -1)
    #
    # If processQueue were to empty a non-empty queue (i.e., take len > 0 and produce len1 = 0),
    # these two constraints would require (maxPrio == -1), which contradicts the invariant inv().
    # The invariant states that if len > 0, then maxPrio == 0.
    #
    # Therefore, to avoid contradiction, processQueue cannot empty a non-empty queue.
    # The simplest model that satisfies this is the identity function, where the state does not change.
    # This model makes the fail condition in the CHC rules unreachable due to the invariant.
    return And(
        len1 == len,
        maxPrio1 == maxPrio,
        minPacketSize1 == minPacketSize
    )