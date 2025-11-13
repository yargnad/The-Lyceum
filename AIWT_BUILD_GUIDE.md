# The Lyceum: AIWT (AI Walkie-Talkie) Build Guide

**Version:** 0.7 - October 21, 2025
**Status:** DRAFT - Qwen 2.5 Integration

## 1. Introduction: The First "Symbolon"

Welcome, rebel. This document outlines the construction of the AI-Enhanced Walkie-Talkie (AIWT), the foundational application of The Lyceum network.

The AIWT is more than a device; it is the "killer app" designed to bootstrap our entire ecosystem. It provides immediate, tangible utility—long-range voice communication without reliance on corporate infrastructure—and serves as the gateway for users to join and organically grow the network. By building an AIWT, you are not just assembling hardware; you are deploying the first node of a new, sovereign commons.

This guide details the two primary paths for building an AIWT, reflecting our core principle: "choose your own level of involvement."

## 2. Path A: The "Scout" AIWT (Phone-Reliant)

The Scout is the low-cost, accessible entry point for every citizen of The Lyceum. It is designed to be affordable and easy to assemble, leveraging the powerful computer you already own: your smartphone.

* **Philosophy:** Maximum accessibility to drive network growth.
* **Approx. Cost:** $25 - $30
* **Core Hardware:** Heltec V4 (ESP32-S3) or similar Meshtastic-compatible board.
* **Core Software:** Standard Meshtastic firmware + The Lyceum mobile client app (forked from the official Meshtastic client).

## 3. Path B: The "Sovereign" AIWT (Self-Contained)

The Sovereign is the aspirational, high-performance device for the dedicated core of our community. It is a true, stand-alone communication tool that requires no other device to function. It is also the first "Pneuma Seed Node."

* **Philosophy:** Maximum sovereignty and a direct contribution to the Pneuma compute network.
* **Approx. Cost:** $120 - $145
* **Core Software:** Base Linux OS (e.g., Armbian) + Meshtastic firmware + On-Device AI Symbolons.

### Sovereign Build: Bill of Materials

| Component | Item | Approx. Cost | Notes |
| :--- | :--- | :--- | :--- |
| **The Brain** | Radxa Zero 3W (4GB/32GB eMMC) | $50 - $75 | Rockchip RK3566 w/ NPU. An Orange Pi Zero 3 is a viable alternative. |
| **The Radio** | Waveshare SX1262 LoRaWAN HAT (915 MHz) | $30 | Stacks directly on the Radxa's GPIO header. |
| **The Display** | Waveshare 1.3inch OLED HAT | $15 | Stacks on top of the LoRa HAT. Has a **5-way joystick & 3 side buttons**. |
| **Power System** | **Seeed Studio Lipo Rider Plus** | $15 | **CRITICAL.** This is our all-in-one USB-C charger and **5V / 2.5A** booster. |
| **The Battery** | 3000mAh Lithium Ion Polymer (LiPo) Battery | $11 | Must have a 2-pin JST-PH 2.0 connector to plug into the Lipo Rider. |
| **The Antenna** | Standard 915 MHz SMA Antenna | Included | Comes with the LoRa HAT. |
| **Misc** | 40-pin GPIO Stacking Header, Wires | $10 | For connecting the HATs and power. |

### Sovereign AI Software: The NPU-Accelerated Stack (v1.1)

A core challenge is running AI models efficiently on-device. This full NPU-accelerated stack is the "secret sauce" of the Sovereign build, ensuring high performance and low battery consumption.

* **Speech-to-Text (STT):** We will use the **[`SenseVoiceSmall-RKNN2`](https://huggingface.co/happyme531/SenseVoiceSmall-RKNN2) model.** This is a lightweight, pre-compiled model **specifically optimized to run on the Rockchip (RKNN) NPU** in our Radxa hardware. This will handle the "hearing" part of our loop.

* **Text-to-Speech (TTS):** We will use the **[`paroli`](https://github.com/marty1885/paroli) library.** This is a blazing-fast TTS engine, also **specifically optimized for the Rockchip NPU.** It is extremely fast (generates speech 5x faster than real-time), has a tiny 35MB footprint, and will handle the "speaking" part of our loop.

* **Routing & Logic (The Moderator):** We will use **Qwen 2.5 3B (Quantized)**. This model fits comfortably within the Radxa's RAM and is powerful enough to act as the local "Router" for the Pneuma network, analyzing user prompts and dispatching them to expert nodes.

This end-to-end NPU pipeline (SenseVoice -> Qwen -> paroli) is a massive technical win. It offloads all heavy AI tasks from the main CPU, which will dramatically improve system responsiveness and battery life.

## 4. Power Management & Message Reception: The "Two Brains" Architecture

The Sovereign AIWT solves the battery life challenge with a "two brains" architecture.

* **Brain #1: The Thinker (Radxa Zero 3W):** The powerful main processor. Spends most of its time in a deep, low-power sleep state.
* **Brain #2: The Listener (SX1262 LoRa Chip):** The dedicated microcontroller on the LoRa HAT. It sips microamps of power and **never sleeps.**

### The "Digital Tripwire" Workflow (Receiving):

1.  **The Vigil:** The Radxa (Thinker) goes to sleep, but first tells the SX1262 (Listener) to watch for incoming messages.
2.  **The Whisper:** A LoRa packet arrives. The always-on SX1262 verifies it and receives it into a small internal buffer.
3.  **The Tripwire:** The SX1262 sends a **hardware interrupt** (an electrical signal) to the Radxa via a GPIO pin.
4.  **The Awakening:** The interrupt instantly wakes the Radxa CPU from its sleep state.
5.  **The Hand-Off:** The Radxa queries the LoRa HAT and retrieves the message from its buffer.
6.  **Action & Return to Sleep:** The Radxa processes the message (displays it, runs TTS), and then its control script commands the OS to return to sleep.

## 5. Sovereign AIWT: Control & UI Concept (v1.0)

The Waveshare OLED HAT provides a rich 8-button control scheme (a 5-way joystick and 3 side buttons). This transforms the device from a simple walkie-talkie into a full handheld communicator.

### Joystick (High-Frequency Actions)

* **Center-Press:** **PTT (Push-to-Talk).**
* **Up/Down:** **Contextual Scroll** (Volume Up/Down or Message Scroll).
* **Left/Right:** **Contextual Switch** (Channel/Contact Switch or Menu Navigation).

### Side Buttons (System-Level Actions)

* **Button 1 (Top): Power / Main Menu.**
* **Button 2 (Middle): "Inbox / Replay"** (Toggles message inbox, replays selected message).
* **Button 3 (Bottom): The "Pneuma Button"** (Activates STT for a direct query to the Pneuma federated AI).

## 6. The Immediate Goal: The "Ping-Pong" Proof-of-Concept (PoC)

1.  **Build the Hardware:** Assemble one Scout and one Sovereign node using the parts lists.
2.  **Establish Radio Link:** Flash both with base Meshtastic firmware and confirm they can exchange simple text messages.
3.  **Implement the "Scout Send":** Fork the Meshtastic mobile client and implement the STT-to-text transmission loop.
4.  **Implement the "Sovereign AI":** Install the `SenseVoice`, `Qwen 2.5`, and `paroli` models on the Sovereign node and write the main control script to tie them to the hardware.
5.  **The Win Condition:** A user speaks into the Scout-paired phone. The Sovereign node receives the text, *converts it to speech, and plays it audibly.* This proves the entire end-to-end concept.

## 7. How to Contribute

This is a living document. We are actively seeking developers and hardware hackers to help:
* Fork the Meshtastic client and build the AIWT user interface.
* **Help benchmark and implement the `SenseVoice` and `paroli` stack on the Radxa Zero 3W.**
* Design and share 3D-printable enclosures for both build paths.

Join us. Let's build the future of communication, together.
