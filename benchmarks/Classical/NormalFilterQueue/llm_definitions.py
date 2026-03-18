# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
def inv(len, maxPrio, minPacketSize):
    len_is_non_negative = (len >= 0)
    empty_state_props = And(maxPrio == -1, minPacketSize == -1)
    non_empty_state_props = And(maxPrio == 0, minPacketSize >= 500)
    state_properties = If(len == 0, empty_state_props, non_empty_state_props)
    return And(len_is_non_negative, state_properties)

def append(prio, packetSize, len, maxPrio, minPacketSize, len1, maxPrio1, minPacketSize1):
    precondition = (len >= 0)
    
    len_trans = (len1 == len + 1)
    
    maxPrio_trans = (maxPrio1 == If(len == 0, prio, If(prio > maxPrio, prio, maxPrio)))
    
    minPacketSize_trans = (minPacketSize1 == If(len == 0, packetSize, If(packetSize < minPacketSize, packetSize, minPacketSize)))
    
    return And(precondition, len_trans, maxPrio_trans, minPacketSize_trans)

def processQueue(len, maxPrio, minPacketSize, len1, maxPrio1, minPacketSize1):
    # This function acts as a no-op, passing the state through.
    # The assertion check is performed on its output variables.
    return And(len1 == len, maxPrio1 == maxPrio, minPacketSize1 == minPacketSize)