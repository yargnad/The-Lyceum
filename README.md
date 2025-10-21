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
