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
* **Sovereignty:** This ensures that only members of our commons can participate in it. The network's security is not based on hiding, but on strong, proven encryption
