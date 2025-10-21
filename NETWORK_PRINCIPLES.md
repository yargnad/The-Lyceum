# The Lyceum: Network Principles (Layer 1)

**Version:** 1.0 - October 21, 2025
**Status:** DRAFT

## 1. Introduction: The Rules of the Commons

This document outlines the fundamental networking principles for The Lyceum's Layer 1 Access Mesh. This layer is built upon the robust, open-source Meshtastic protocol. Understanding these principles is key to understanding how our network remains private, resilient, and efficient.

The network is designed to be a "smart rumor mill," not a dumb one. It has built-in mechanisms to ensure messages are delivered to their intended recipients and then die a quiet death, preventing the network from being polluted by a flood of old, repeating data.

## 2. Principle 1: The Cryptographic Boundary (The Private Channel)

The Lyceum does not operate on the public, default Meshtastic channel. Our network is a private, encrypted commons, and its borders are cryptographic.

* **Pre-Shared Key (PSK):** All communication is encrypted using a secret Pre-Shared Key (PSK). This key, combined with our channel name, defines the network.
* **Access Control:** Only a device that has been explicitly configured with The Lyceum's PSK can decrypt, read, and relay our network's traffic. Any LoRa device without this key will only hear indecipherable static.
* **Sovereignty:** This ensures that only members of our commons can participate in it. The network's security is not based on hiding, but on strong, proven encryption.

## 3. Principle 2: Node Addressing & Message Types

Every device on the network has a unique, randomly generated Node ID (e.g., `!a7b3c9d1`). This is its address within the commons.

* **Broadcast (The Town Crier):** A message sent to the entire channel. Every node that hears it will process it. This is for community-wide information.
* **Direct Message (The Sealed Letter):** A message addressed to a specific Node ID. While it is relayed by the public mesh, the packet header instructs all nodes except the intended recipient to simply forward it without "opening" it. This is the primary method for point-to-point communication, such as our AIWT.

## 4. Principle 3: Flood Prevention & Message Lifecycle

To prevent a message from echoing through the network forever, the protocol uses three overlapping systems:

1.  **The "Seen" List (Short-Term Memory):**
    * Every data packet has a unique random ID.
    * Every node maintains a list of the last few dozen packet IDs it has seen.
    * If a node hears a packet with an ID on its list, it immediately discards it, preventing endless relay loops. This is the network's primary defense against message storms.

2.  **The Hop Limit (Guaranteed Lifespan):**
    * Every packet is created with a "Hop Limit" (e.g., a value of 7).
    * Each time a node relays the packet, it decrements this value by one.
    * A node will not relay a packet if its hop limit is 1 or 0.
    * This ensures every packet is guaranteed to die after a certain number of relays, preventing a local message from needlessly propagating across a continent.

3.  **The Acknowledgement or "ACK" (Reliable Delivery):**
    * When a node receives a **direct message** addressed to it, it sends a small, new message back into the mesh called an Acknowledgement (ACK).
    * This ACK packet informs the network that the original message has been successfully delivered.
    * Other nodes that hear this ACK can then stop trying to relay the original message and can purge it from their queues. This is the "clean-up crew" that makes direct communication efficient.

These principles, working in concert, create the resilient and private foundation upon which the rest of The Lyceum is built.
