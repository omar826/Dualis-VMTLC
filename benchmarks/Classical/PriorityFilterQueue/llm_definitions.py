# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
from z3 import *

def inv(len, minPrio, maxPacketSize):
    # The invariant captures the state of the queue.
    # It can either be empty, with initial values, or non-empty with specific properties.
    empty_state = And(len == 0, minPrio == -1, maxPacketSize == -1)
    
    # If the queue is not empty (len > 0), then due to the client's usage:
    # - The minimum priority will always be 1, as only packets with prio=1 are added.
    # - The maximum packet size will be constrained by the client's check (0 < packetSize < 500).
    non_empty_state = And(len > 0, 
                          minPrio == 1, 
                          maxPacketSize > 0, 
                          maxPacketSize < 500)
                          
    return Or(empty_state, non_empty_state)

def append(prio, packetSize, len, minPrio, maxPacketSize, len1, minPrio1, maxPacketSize1):
    # This defines the general behavior of an append operation.
    
    # The length is always incremented.
    len_update = (len1 == len + 1)
    
    # The new minPrio is the minimum of the old minPrio and the new prio.
    # If the queue was empty, the new minPrio is simply the new prio.
    minPrio_update = If(len == 0,
                        minPrio1 == prio,
                        minPrio1 == If(prio < minPrio, prio, minPrio))
                        
    # The new maxPacketSize is the maximum of the old maxPacketSize and the new packetSize.
    # If the queue was empty, the new maxPacketSize is simply the new packetSize.
    maxPacketSize_update = If(len == 0,
                              maxPacketSize1 == packetSize,
                              maxPacketSize1 == If(packetSize > maxPacketSize, packetSize, maxPacketSize))

    return And(len_update, minPrio_update, maxPacketSize_update)

def processQueue(len, minPrio, maxPacketSize, len1, minPrio1, maxPacketSize1):
    # This function models the processing and emptying of the queue.
    # As indicated by the assertion, when the queue is processed, its length becomes 0,
    # and the other state variables are reset to their initial values.
    return And(len1 == 0, minPrio1 == -1, maxPacketSize1 == -1)