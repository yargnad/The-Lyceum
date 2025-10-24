# The Lyceum: AIWT (AI Walkie-Talkie) Build Guide

**Version:** 0.4 - October 21, 2025
**Status:** DRAFT - Hardware & UI Concept

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
* **Core Software:** Base Linux OS (e.g., Armbian) + Meshtastic firmware + on-device AI models for STT/TTS.

### Sovereign Build: Bill of Materials

| Component | Item | Approx. Cost | Notes |
| :--- | :--- | :--- | :--- |
| **The Brain** | Radxa Zero 3W (4GB/32GB eMMC) | $50 - $75 | The target model. An Orange Pi Zero 3 is a viable alternative if this is unavailable. |
| **The Radio** | Waveshare SX1262 LoRaWAN HAT (915 MHz) | $30 | Stacks directly on the Radxa's GPIO header. |
| **The Display** | Waveshare 1.3inch OLED HAT | $15 | Stacks on top of the LoRa HAT. Has a **5-way joystick & 3 side buttons**. |
| **Power System** | **Seeed Studio Lipo Rider Plus** | $15 | **CRITICAL.** This is our all-in-one USB-C charger and **5V / 2.5A** booster. |
| **The Battery** | 3000mAh Lithium Ion Polymer (LiPo) Battery | $11 | Must have a 2-pin JST-PH 2.0 connector to plug into the Lipo Rider. |
| **The Antenna** | Standard 915 MHz SMA Antenna | Included | Comes with the LoRa HAT. |
| **Misc** | 40-pin GPIO Stacking Header, Wires | $10 | For connecting the HATs and power. |

### Sovereign Feature: Emergency Power Bank

The Seeed Studio Lipo Rider Plus board includes a **USB-A output port**, allowing your Sovereign AIWT to function as an emergency 3000mAh power bank for charging a phone or other device.

**Usage Caveat:** The Lipo Rider is rated for a **2.5A *total* output.** Charge external devices when the AIWT is in standby. Do not attempt to charge a device while also running high-intensity tasks on the Radxa, as this can cause a system-wide brownout.

## 4. Power Management & Message Reception: The "Two Brains" Architecture

A critical challenge for a battery-powered device is receiving messages without draining the battery. The Sovereign AIWT solves this with a "two brains" architecture.

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

The Waveshare OLED HAT provides a rich 8-button control scheme (a 5-way joystick and 3 side buttons). This transforms the device from a simple walkie-talkie into a full handheld communicator. The proposed v1.0 control map separates real-time actions (joystick) from system-level actions (side buttons).

### Joystick (High-Frequency Actions)

* **Center-Press:** **PTT (Push-to-Talk).** This is the primary "do the main thing" button.
* **Up/Down:** **Contextual Scroll.**
    * On "Live" Screen: Controls **Volume Up / Down.**
    * In "Inbox" Screen: **Scrolls through saved messages.**
* **Left/Right:** **Contextual Switch.**
    * On "Live" Screen: **Switches Channel or Contact.**
    * In Menu: Navigates menus.

### Side Buttons (System-Level Actions)

* **Button 1 (Top): Power / Main Menu.**
    * *Short Press:* Opens the main settings menu (e.g., "View Node ID," "Set Channel," "Reboot").
    * *Long Press (3 sec):* Initiates the safe **Shutdown / Power On** sequence.
* **Button 2 (Middle): "Inbox / Replay."**
    * *Short Press:* Toggles between the "Live" screen and the "Message Inbox."
    * *In Inbox:* Acts as the **"Replay"** button for the selected message.
* **Button 3 (Bottom): The "Pneuma Button."**
    * *Short Press:* Activates STT for a direct query to the Pneuma federated AI (e.g., "Pneuma, what's the network status?").

## 6. The Immediate Goal: The "Ping-Pong" Proof-of-Concept (PoC)

1.  **Build the Hardware:** Assemble one Scout and one Sovereign node using the parts lists.
2.  **Establish Radio Link:** Flash both with base Meshtastic firmware and confirm they can exchange simple text messages.
3.  **Implement the "Scout Send":** Fork the Meshtastic mobile client and implement the STT-to-text transmission loop.
4.  **The Win Condition:** A user speaks into the Scout-paired phone. The Sovereign node receives the message as text. This proves the core concept is viable.

## 7. How to Contribute

This is a living document. We are actively seeking developers and hardware hackers to help:
* Fork the Meshtastic client and build the AIWT user interface.
* Research and benchmark lightweight, open-source STT/TTS models for the Sovereign build.
* Design and share 3D-printable enclosures for both build paths.

Join us. Let's build the future of communication, together.
