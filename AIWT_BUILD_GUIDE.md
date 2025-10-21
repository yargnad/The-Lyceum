# The Lyceum: AIWT (AI Walkie-Talkie) Build Guide

**Version:** 0.2 - October 21, 2025
**Status:** DRAFT - Architectural Workflow

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

### Workflow:

The Scout acts as a highly efficient "radio modem" for your phone. The phone's processor handles all STT/TTS operations, and the Scout hardware manages the LoRa radio and Bluetooth connection.

## 3. Path B: The "Sovereign" AIWT (Self-Contained)

The Sovereign is the aspirational, high-performance device for the dedicated core of our community. It is a true, stand-alone communication tool that requires no other device to function. It is also the first "Pneuma Seed Node."

* **Philosophy:** Maximum sovereignty and a direct contribution to the Pneuma compute network.
* **Approx. Cost:** $80 - $100+
* **Core Hardware:** Radxa Zero 3W (or similar powerful SBC with an NPU) + a compatible LoRa radio HAT.
* **Core Software:** Base Linux OS (e.g., Armbian) + Meshtastic firmware + on-device AI models for STT/TTS.

### Workflow (Sending):

The Sovereign handles all processing on-device. The user speaks, the Radxa's NPU/CPU converts speech to text, and the LoRa HAT transmits the resulting packet.

## 4. Power Management & Message Reception: The "Two Brains" Architecture

A critical challenge for a battery-powered device is receiving messages without draining the battery. A high-power application processor (like the Radxa) cannot listen for radio signals while in a deep sleep. The Sovereign AIWT solves this with a "two brains" architecture.

* **Brain #1: The Thinker (Radxa Zero 3W):** This is the powerful main processor. It runs the Linux OS and the AI models. To preserve power, it spends most of its time in a deep, low-power sleep state.
* **Brain #2: The Listener (SX1262 LoRa Chip):** The chip on the LoRa HAT is a dedicated microcontroller in its own right. It runs simple firmware and sips microamps of power. **This brain never sleeps.**

### The "Digital Tripwire" Workflow (Receiving):

1.  **The Vigil:** The Radxa (Thinker) puts itself to sleep. Before it does, it configures the SX1262 (Listener) to watch for incoming LoRa packets on our private channel.
2.  **The Whisper:** A LoRa packet arrives. The always-on SX1262 detects it, verifies it's for our channel, and receives it into a small internal memory buffer.
3.  **The Tripwire:** The SX1262 now wakes the main processor by sending a **hardware interrupt**—an electrical signal over a specific GPIO pin connecting the HAT to the Radxa.
4.  **The Awakening:** The interrupt instantly wakes the Radxa CPU from its sleep state.
5.  **The Hand-Off:** The Radxa's software queries the LoRa HAT, which then transfers the message from its buffer to the Radxa's main memory.
6.  **Action & Return to Sleep:** The Radxa is now fully awake. It processes the message (displays it, runs TTS). Once complete, its control script commands the OS to return to a deep sleep, and the cycle repeats.

This co-processor model provides the power of a full computer when needed and the battery efficiency of a dedicated microcontroller during idle periods.

## 5. The Immediate Goal: The "Ping-Pong" Proof-of-Concept (PoC)

Our first practical step is to build one of each device and demonstrate basic functionality.

1.  **Build the Hardware:** Assemble one Scout and one Sovereign node.
2.  **Establish Radio Link:** Flash both with base Meshtastic firmware and confirm they can exchange simple text messages.
3.  **Implement the "Scout Send":** Fork the Meshtastic mobile client and implement the STT-to-text transmission loop.
4.  **The Win Condition:** A user speaks into the Scout-paired phone. The Sovereign node receives the message as text. This proves the core concept is viable.

## 6. How to Contribute

This is a living document. We are actively seeking developers and hardware hackers to help:
* Fork the Meshtastic client and build the AIWT user interface.
* Research and benchmark lightweight, open-source STT/TTS models for the Sovereign build.
* Design and share 3D-printable enclosures for both build paths.

Join us. Let's build the future of communication, together.
