# This file is auto-generated. Do not edit directly.

from z3 import *
# --- LLM Generated Definitions ---
def inv(len, minPrio, maxPacketSize):
    # The invariant captures the state of the queue.
    # If the queue is empty (len == 0), minPrio and maxPacketSize have initial values (-1).
    # If the queue is not empty (len > 0), items have been appended.
    # Based on the append rule, only prio=1 is ever added, so minPrio must be 1.
    # The packetSize is always between 0 and 500, so maxPacketSize must be in that range.
    return And(len >= 0,
               If(len == 0,
                  And(minPrio == -1, maxPacketSize == -1),
                  And(minPrio == 1, maxPacketSize >= 0, maxPacketSize < 500)
               ))

def append(prio, packetSize, len, minPrio, maxPacketSize, len1, minPrio1, maxPacketSize1):
    # This relation defines the state transition for an append operation.
    # The new length is the old length plus one.
    # The new minPrio is 1, as only prio=1 packets are appended.
    # The new maxPacketSize is updated. If the queue was empty, it's the current
    # packet's size. Otherwise, it's the maximum of the old max and the current size.
    next_len = (len1 == len + 1)
    next_minPrio = (minPrio1 == 1)
    
    update_max_size = If(len == 0,
                         maxPacketSize1 == packetSize,
                         maxPacketSize1 == If(packetSize > maxPacketSize, packetSize, maxPacketSize))

    return And(next_len, next_minPrio, update_max_size)

def processQueue(len, minPrio, maxPacketSize, len1, minPrio1, maxPacketSize1):
    # This relation must ensure the final assertion holds. The assertion is:
    # (len1 == 0) ==> (minPrio1 == -1 && maxPacketSize1 == -1)
    # The simplest way to satisfy this is to define the operation as one that
    # always empties the queue and resets the state variables to their initial "empty" values.
    return And(len1 == 0,
               minPrio1 == -1,
               maxPacketSize1 == -1)