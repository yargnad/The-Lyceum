# The Lyceum: AIWT (AI Walkie-Talkie) Build Guide

**Version:** 0.1 - October 21, 2025
**Status:** Conceptual Workflow & Proof-of-Concept Plan

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

The Scout acts as a highly efficient "radio modem" for your phone.

1.  **User speaks** into their smartphone.
2.  The **Lyceum client app** on the phone uses the phone's native Speech-to-Text (STT) engine to convert the speech to a text string.
3.  The app sends this **text string** via Bluetooth to the Scout hardware.
4.  The Scout's LoRa radio transmits the text packet over **The Lyceum's Layer 1 Access Mesh.**
5.  A recipient node receives the text packet and sends it to their own phone via Bluetooth.
6.  The recipient's Lyceum client app uses the phone's native Text-to-Speech (TTS) engine to play the message as audible voice.

## 3. Path B: The "Sovereign" AIWT (Self-Contained)

The Sovereign is the aspirational, high-performance device for the dedicated core of our community. It is a true, stand-alone communication tool that requires no other device to function. It is also the first "Pneuma Seed Node."

* **Philosophy:** Maximum sovereignty and a direct contribution to the Pneuma compute network.
* **Approx. Cost:** $80 - $100+
* **Core Hardware:** Radxa Zero 3W (or similar powerful SBC with an NPU) + a compatible LoRa radio HAT.
* **Core Software:** Base Linux OS (e.g., Armbian) + Meshtastic firmware + on-device AI models for STT/TTS.

### Workflow:

The Sovereign handles all processing on-device.

1.  **User speaks** into the Sovereign's integrated (or attached) microphone.
2.  The **Radxa's processor and NPU** run an embedded STT engine, converting speech to a text string directly on the device.
3.  The device's LoRa radio transmits the text packet over the **Layer 1 Access Mesh.**
4.  A recipient node receives the packet.
5.  If the recipient is also a Sovereign, its onboard TTS engine converts the text back to voice. If the recipient is a Scout, the text is passed to their phone for TTS conversion.
6.  **Pneuma Contribution:** When plugged into power at home, the Sovereign's NPU becomes available to the network, running a "Pneuma Guardian" Symbolon to help vet apps and secure the commons.

## 4. The Immediate Goal: The "Ping-Pong" Proof-of-Concept (PoC)

Our first practical step is to build one of each device and demonstrate basic functionality.

1.  **Build the Hardware:** Assemble one Scout and one Sovereign node.
2.  **Establish Radio Link:** Flash both with base Meshtastic firmware and confirm they can exchange simple text messages.
3.  **Implement the "Scout Send":** Fork the Meshtastic mobile client and implement the STT-to-text transmission loop.
4.  **The Win Condition:** A user speaks into the Scout-paired phone. The Sovereign node receives the message as text. This proves the core concept is viable.

## 5. How to Contribute

This is a living document and an open invitation. We are actively seeking developers and hardware hackers to help:
* Fork the Meshtastic client and build the AIWT user interface.
* Research and benchmark lightweight, open-source STT/TTS models that can run on the Sovereign's hardware.
* Design and share 3D-printable enclosures for both build paths.

Join us. Let's build the future of communication, together.
