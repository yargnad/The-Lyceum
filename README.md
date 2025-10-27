# The Lyceum Network

**Your Voice. Your Network. Your AI.**

The Lyceum is an open-source, community-owned, and decentralized communication and compute network. We are building a resilient, privacy-first alternative to the corporate internet. This project is a public commons, not a company.

## Our Doctrine: Radical Resourcefulness

We reject the endless cycle of engineered obsolescence. The Lyceum is built to honor and utilize any hardware you can contribute, from a brand-new single-board computer to a dusty laptop in your closet. In our commons, nothing is wasted.

## How to Participate: Choose Your Role

There are many ways to contribute, from simply using the network to providing its core compute power. Here’s a guide to the hardware paths:

| Role / Tier         | Example Device(s)                  | Approx. Cost             | Key Compute Resource | Ideal "Pneuma" Task                                |
| :------------------ | :--------------------------------- | :----------------------- | :------------------- | :------------------------------------------------- |
| **"Scout"** | Heltec V4 (ESP32-S3)               | $25 - $30                | Bluetooth to Smartphone | **Client Only.** Uses phone for STT/TTS.           |
| **"Sovereign AIWT"**| Radxa Zero 3W + LoRa HAT           | $80 - $100               | **NPU** (on-device AI) | **Pneuma Guardian (Vetting):** On-device STT/TTS, App Vetting |
| **"GPU Guardian"** | Orange Pi Zero 3 + HAT             | $75 - $95                | **Mali GPU** (Parallel) | **Expert Symbolons:** Image/Signal processing      |
| **"Legacy Guardian"** | Old Gaming PC/Laptop (GTX 960m+) | **$0 (Existing Hardware)** | **CUDA Cores** | **Specialist Experts:** Audio, small CV/NLP models |
| **"Genesis Node"** | Orange Pi 5 / Rock 5B              | $150+                    | **High-Power NPU & GPU** | **Core Host:** Gating Network & multiple Experts   |

## 🛡 Prior Art: Key Innovations
The Lyceum introduces several novel concepts:

1. **Tiered, Resourceful Mesh Architecture**:
   - Unlike traditional mesh networks (e.g., Helium, Althea), The Lyceum is designed to **leverage any hardware**, from ESP32 "Scouts" to repurposed gaming PCs ("Legacy Guardians").
   - **Patent-busting detail**: The network dynamically assigns tasks (e.g., STT/TTS, AI vetting) based on a device’s capabilities (NPU, GPU, CUDA cores), not just its bandwidth.

2. **AI-Enhanced Walkie-Talkie (AIWT)**:
   - Combines **offline speech-to-text (Whisper.cpp/Coqui)** with **LoRa mesh networking** (Meshtastic fork) in a single, low-cost device.
   - **Patent-busting detail**: Uses **token rewards** to incentivize relaying *and* compute sharing (e.g., CPU/GPU for AI tasks).

3. **Pneuma Daemon & Symbolon Framework**:
   - A lightweight background service ("Pneuma Daemon") that enables **modular AI tasks** (e.g., message vetting, serendipity engines) across heterogeneous hardware.
   - **Patent-busting detail**: Tasks are assigned via a **capability-based matching system** (e.g., "This node has a Mali GPU—route image processing here").

4. **Tokenized Contribution Ledger**:
   - Rewards **not just for bandwidth** (like Helium) but for **compute, storage, and AI contributions**.
   - **Patent-busting detail**: Tokens are logged in a **local-first, SQLite-ledger** (decentralized, no blockchain bloat).

5. **MURS as a Backhaul**:
   - Plans to use **MURS radio** (unlicensed, encrypted) for long-range backhaul, avoiding reliance on the internet or licensed spectrum (e.g., HAM).
   - **Patent-busting detail**: MURS nodes act as **bridges between LoRa "islands,"** with tokens incentivizing their deployment.

6. **Ethical AI Guardrails**:
   - AI tasks (e.g., moderation, serendipity) are **locally vetted** by users, not centralized algorithms.
   - **Patent-busting detail**: Users can **opt into "Expert Symbolons"** (e.g., "I’ll vet messages for my local mesh").

## 📜 Prior Art Timeline
- **Oct 2025**: Initial brainstorming and GitHub repo creation.
- **[Future Date]**: First functional prototype (AIWT + LoRa mesh).
- **[Future Date]**: MURS backhaul integration.

## 🚀 Getting Started: The AI Walkie-Talkie

The best way to join the network is to build our first application: the AI-Enhanced Walkie-Talkie.

1.  **Get the Hardware:** Pick a path from the matrix above. We recommend starting with a **"Scout"** build (e.g., a Heltec V4) for the lowest cost of entry.
2.  **Flash Meshtastic:** Follow the excellent Meshtastic documentation to flash the latest firmware onto your device.
3.  **Join the Lyceum Development:** Our immediate goal is to fork the Meshtastic client and build the STT/TTS "walkie-talkie" functionality. All development will happen here.

## How to Contribute

* **Developers:** Fork this repository! Help us build the AI Walkie-Talkie, the universal Pneuma Daemon, and the Symbolon app framework.
* **Hardware Hackers:** Design and share schematics for our self-contained devices and MURS backbone nodes.
* **Everyone:** Buy or repurpose a node! The single most important contribution is expanding the physical network.

## License

This project is licensed under the **GNU General Public License v3.0**. This ensures that The Lyceum and any derivative works will always remain free and open source. See the `LICENSE` file for the full text.
