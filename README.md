# The Lyceum Network

**Your Voice. Your Network. Your AI.**

The Lyceum is an open-source, community-owned, and decentralized communication and compute network. We are building a resilient, privacy-first alternative to the corporate internet. This project is a public commons, not a company.

## 1. Our Doctrine: Radical Resourcefulness

We reject the endless cycle of engineered obsolescence. The Lyceum is built to honor and utilize any hardware you can contribute, from a brand-new single-board computer to a dusty laptop in your closet. In our commons, nothing is wasted.

## 2. Our Prior Art: A Declaration of the Commons

This document and its associated files, in this public repository, establish the prior art for a novel, multi-layered, decentralized system. By making this knowledge public, we permanently place it in the commons and defend it from corporate capture.

Our claim of prior art covers the specific, interlocking architecture of:

1.  **A Hybrid Voice/Data System (The AIWT):** A device that enables long-range voice communication over a low-bandwidth (LoRa) mesh by performing on-device Speech-to-Text (STT), transmitting the resulting text packet, and performing Text-to-Speech (TTS) on the receiving device.
2.  **A Dual-Path Hardware Model:** A two-pronged implementation for this device: a low-cost, phone-reliant "Scout" (e.g., ESP32-S3) and a high-performance, self-contained "Sovereign" (e.g., Radxa Zero 3W).
3.  **A Specific, NPU-Accelerated Software Stack:** The use of specialized, NPU-accelerated models on Rockchip hardware to achieve this efficiently, specifically a stack pairing a **`SenseVoice-RKNN`** model (for STT) with the **`paroli`** library (for TTS).
4.  **A "Two-Brain" Power Architecture:** A low-power-standby model for the "Sovereign" node, where a high-power "Thinker" (the Radxa CPU) is put to sleep and is woken by a hardware interrupt from a low-power "Listener" (the SX1262 LoRa co-processor) upon message receipt.
5.  **A "Proof-of-Utility" Compute Network ("Pneuma"):** A federated compute network built from the idle resources (NPU, GPU, CPU) of its own nodes, where these "Guardian" nodes are rewarded via a lightweight, "Anti-Blockchain" ledger.
6.  **A Vetted Application Ecosystem ("Symbolon"):** A system for hosting on-device applications ("Symbolons") that are vetted for security by the "Pneuma" network's federated guardians.

## 3. How to Participate: Choose Your Role

There are many ways to contribute. This hardware guide is a living document for our "radical resourcefulness" doctrine.

| Role / Tier | Example Device(s) | Approx. Cost | Key Compute Resource | Ideal "Pneuma" Task |
| :--- | :--- | :--- | :--- | :--- |
| **"Scout"** | Heltec V4 (ESP32-S3) | $25 - $30 | Bluetooth to Smartphone | **Client Only.** Uses phone for STT/TTS. |
| **"Sovereign AIWT"**| Radxa Zero 3W + LoRa HAT | $80 - $100 | **NPU** (on-device AI) | **Pneuma Guardian (Vetting):** On-device AIWT, App Vetting |
| **"GPU Guardian"** | Orange Pi Zero 3 + HAT | $75 - $95 | **Mali GPU** (Parallel) | **Expert Symbolons:** Image/Signal processing |
| **"Legacy Guardian"** | Old Gaming PC/Laptop (GTX 960m+) | **$0 (Existing Hardware)** | **CUDA Cores** | **Specialist Experts:** Audio, small CV/NLP models |
| **"Genesis Node"** | Orange Pi 5 / Rock 5B | $150+ | **High-Power NPU & GPU** | **Core Host:** Gating Network & multiple Experts |

## 4. Getting Started: The AI Walkie-Talkie

The best way to join is to build our foundational app. See the `AIWT_BUILD_GUIDE.md` for full details.

## 5. How to Contribute

* **Developers:** Fork this repository! Help us build the AIWT, the universal Pneuma Daemon, and the Symbolon app framework.
* **Hardware Hackers:** Design and share 3D-printable enclosures and antenna designs.
* **Everyone:** Buy or repurpose a node! The single most important contribution is expanding the physical network.

## 6. License

This project is licensed under the **GNU General Public License v3.0**. This ensures that The Lyceum and any derivative works will always remain free and open source. See the `LICENSE` file for the full text.
