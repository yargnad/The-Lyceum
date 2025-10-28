# The Lyceum: Network Principles (Layer 1)

**Version:** 1.1 - October 21, 2025
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

## 5. Rejected Bands: Why Not CBRS?

A core tenet of our "radical resourcefulness" is to use all available tools. However, some tools are ideological traps. The Lyceum will **not** use the CBRS band (3.5 GHz) for any layer of the network.

CBRS is a "poisoned chalice." It appears to be a powerful, open band, but it is fundamentally incompatible with our core principles of sovereignty, resilience, and privacy.

* **The "Leash":** To use CBRS, every node is legally required to have a constant **internet connection** to a centralized, corporate-run cloud database called a **Spectrum Access System (SAS)**.
* **The Deal-Breakers:**
    1.  **Fails Resilience:** If the internet goes down, the SAS cannot be reached, and all CBRS radios are legally required to **stop transmitting.** The network dies when it's needed most.
    2.  **Fails Sovereignty:** It is a **permissioned** system. We would have to ask a corporate entity (the SAS operator) for permission to speak. This is an unacceptable compromise.
    3.  **Fails Privacy:** It is a surveillance architecture. Every node must report its identity and exact GPS location to a central database.

CBRS is a tool for extending the corporatocracy's internet, not for building a sovereign alternative. The Lyceum will *only* be built on truly unlicensed, **permissionless** bands (like 900 MHz ISM and 5 GHz UNII) where our right to communicate is guaranteed by the hardware we own, not by a corporate cloud service.
