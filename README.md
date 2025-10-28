# The Lyceum Network

**Author:** Dan Gray, The Authentic Rebellion
**Version:** 1.5 - October 21, 2025
**Status:** DRAFT - Critical Update: Layer 3 Architecture

## 1. Our Doctrine: Radical Resourcefulness

We reject the endless cycle of engineered obsolescence. The Lyceum is built to honor and utilize any hardware you can contribute, from a brand-new single-board computer to a dusty laptop in your closet. In our commons, nothing is wasted.

## 2. Our Prior Art: A Declaration of the Commons

This document and its associated files, in this public repository, establish the prior art for a novel, multi-layered, decentralized system. By making this knowledge public, we permanently place it in the commons and defend it from corporate capture.

Our claim of prior art covers the specific, interlocking architecture of:

1.  **A Hybrid Voice/Data System (The AIWT):** A device that enables long-range voice communication over a low-bandwidth (LoRa) mesh by performing on-device Speech-to-Text (STT), transmitting the resulting text packet, and performing Text-to-Speech (TTS) on the receiving device.
2.  **A Specific, NPU-Accelerated Software Stack:** The use of specialized, NPU-accelerated models on Rockchip hardware to achieve this efficiently, specifically a stack pairing a **`SenseVoice-RKNN`** model (for STT) with the **`paroli`** library (for TTS).
3.  **A "Two-Brain" Power Architecture:** A low-power-standby model for the "Sovereign" node, where a high-power "Thinker" (the Radxa CPU) is put to sleep and is woken by a hardware interrupt from a low-power "Listener" (the SX1262 LoRa co-processor).
4.  **A "Proof-of-Utility" Compute Network ("Pneuma"):** A federated compute network built from the idle resources (NPU, GPU, CPU) of its own nodes, operating on an "Anti-Blockchain" model where a lightweight ledger rewards verifiable utility.
5.  **A "Two-Path Layer 3 Backbone":** A novel L3 architecture using unlicensed bands to create encrypted, long-haul Point-to-Point (PTP) links, specifically using **900 MHz LoRa PTP** for resilient NLOS connections and **5 GHz Wi-Fi PTP** for high-bandwidth LOS connections.
6.  **A Vetted Application Ecosystem ("Symbolon"):** A system for hosting on-device, containerized applications ("Symbolons") that are vetted for security and performance by the "Pneuma" network's federated "Guardian" nodes.

## 3. How It Works (The Three Layers)

The network operates on a unique multi-layered architecture:

1.  **Access Mesh (LoRa):** The base layer for everyone. A long-range, low-power mesh for text, GPS, and sensor data.
2.  **Utility Fabric (Wi-Fi HaLow):** A higher-bandwidth local layer for local applications and the home of our federated AI, "Pneuma."
3.  **Backbone Link (Two-Path Model):** A resilient, encrypted, long-distance backhaul connecting regional clusters. This replaces our previous (legally non-viable) MURS concept. Operators choose the best path for their terrain:
    * **900 MHz LoRa PTP:** For resilient, low-bandwidth links *without* line-of-sight (NLOS).
    * **5 GHz Wi-Fi PTP:** For massive, fiber-speed bandwidth *with* clear line-of-sight (LOS).

## 4. How to Participate: Choose Your Role

This hardware guide is a living document for our "radical resourcefulness" doctrine. (See `whitepaper.md` or v1.4 for the full hardware matrix).

## 5. Getting Started: The AI Walkie-Talkie

The best way to join is to build our foundational app. See the `AIWT_BUILD_GUIDE.md` for full details.

## 6. How to Contribute

* **Developers:** Fork this repository! Help us build the AIWT, the universal Pneuma Daemon, and the Symbolon app framework.
* **Hardware Hackers:** Design and share 3D-printable enclosures and high-gain antennas for our L1 devices and L3 backbone links.
* **Everyone:** Buy or repurpose a node! The single most important contribution is expanding the physical network.

## 7. License

This project is licensed under the **GNU General Public License v3.0**. This ensures that The Lyceum and any derivative works will always remain free and open source. See the `LICENSE` file for the full text.
