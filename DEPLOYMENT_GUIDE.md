# The Lyceum: Deployment Guide

**Version:** 0.1 - Draft
**Status:** DRAFT - Initial Scaffolding

## 1. Introduction

This guide provides a practical playbook for setting up Lyceum hardware, flashing software images, and planning network topology. It covers all three device tiers:

- **Scout AIWT** (Phone-Reliant): $25-30, entry-level mesh node
- **Sovereign AIWT** (Self-Contained): $120-145, full-stack AI node
- **Guardian Node** (Backbone): High-power Pneuma node for federated AI

## 2. Hardware Setup

### 2.1 Scout AIWT Assembly

**Components:**

| Item | Model | Notes |
|------|-------|-------|
| LoRa Board | Heltec V4 (ESP32-S3) | Pre-flashed with Meshtastic |
| Antenna | 915 MHz SMA | Included with board |
| Case | 3D Printed | See `/hardware/enclosures/scout/` |
| Battery | 18650 LiPo | Optional for portable use |

**Steps:**

1. Flash Meshtastic firmware using web flasher: [flasher.meshtastic.org](https://flasher.meshtastic.org)
2. Configure The Lyceum channel and PSK via phone app
3. (Optional) Print enclosure and assemble

### 2.2 Sovereign AIWT Assembly

**Components:**

| Item | Model | Approx. Cost |
|------|-------|--------------|
| Brain | Radxa Zero 3W (4GB) | $50-75 |
| Radio | Waveshare SX1262 HAT | $30 |
| Display | Waveshare 1.3" OLED HAT | $15 |
| Power | Seeed Studio Lipo Rider Plus | $15 |
| Battery | 3000mAh LiPo (JST-PH 2.0) | $11 |
| Antenna | 915 MHz SMA | Included |

**Assembly Steps:**

1. Stack the HATs onto the Radxa Zero 3W GPIO header
2. Connect the Lipo Rider to the Radxa via USB-C
3. Connect the LiPo battery to the Lipo Rider
4. (Optional) Print enclosure and assemble

### 2.3 Guardian Node Setup

Guardian nodes are repurposed computers providing Pneuma compute resources.

**Minimum Specs:**

- 4GB RAM (8GB+ recommended for Cortex jobs)
- Any x86_64 or ARM64 CPU
- Optional: GPU for accelerated inference

**Recommended Hardware:**

- Old laptop with working battery (built-in UPS!)
- Orange Pi 5 (RK3588 NPU)
- Any Rockchip-based SBC with NPU

## 3. Software Installation

### 3.1 Sovereign AIWT Image

1. **Download the base image:**

   ```bash
   # TODO: Host image at lyceum mirrors
   wget https://lyceum.example.org/images/sovereign-v0.1.img.xz
   ```

2. **Flash to eMMC or SD card:**

   ```bash
   xzcat sovereign-v0.1.img.xz | sudo dd of=/dev/sdX bs=4M status=progress
   ```

3. **First boot configuration:**
   - Connect via serial console (115200 baud)
   - Set hostname, WiFi, and Lyceum channel

4. **Download AI models:**

   ```bash
   # Run as root on the Sovereign device
   lyceum-setup download-models
   ```

### 3.2 Guardian Daemon

1. **Install dependencies:**

   ```bash
   pip install lyceum-guardian
   ```

2. **Configure and run:**

   ```bash
   lyceum-guardian init --node-id "!my_guardian"
   lyceum-guardian run
   ```

## 4. Network Topology Planning

### 4.1 Layer 1 Mesh (LoRa)

- **Range:** 1-5 km depending on terrain
- **Placement:** Elevate antennas above obstructions
- **Coverage:** Plan for overlapping ranges between nodes

### 4.2 Layer 2 Fabric (Wi-Fi HaLow)

- **Range:** 100-500m
- **Use case:** Local neighborhood connectivity
- **Guardians:** Should have HaLow capability for local Pneuma jobs

### 4.3 Layer 3 Backbone

**Two-Path Model:**

| Path | Technology | Range | Bandwidth | Use Case |
|------|------------|-------|-----------|----------|
| Resilience | 900 MHz LoRa PTP | 10-30 km NLOS | 10 kbps | Ledger sync, Reflex jobs |
| Bandwidth | 5 GHz Wi-Fi PTP | 5-15 km LOS | 100+ Mbps | Cortex jobs, bulk data |

**Backbone Planning Tips:**

- Use high-gain directional antennas for PTP links
- Mount antennas at the highest practical point
- Survey line-of-sight before installation

## 5. Security Configuration

### 5.1 Lyceum PSK Setup

All Layer 1 devices share a Pre-Shared Key (PSK):

```bash
# Generate a new PSK (32 bytes)
openssl rand -hex 32

# Configure via Meshtastic CLI
meshtastic --setAESkey <your-32-byte-hex>
```

### 5.2 AES-GCM for Pneuma

Layer 2/3 traffic uses per-session ECDH-derived keys. Configure the root key:

```bash
lyceum-config set-key --type pneuma --key <your-key>
```

## 6. Troubleshooting

| Issue | Possible Cause | Solution |
|-------|---------------|----------|
| No LoRa reception | Wrong frequency/SF | Check regional settings |
| STT not working | Model not loaded | Run `lyceum-setup download-models` |
| TTS silent | Audio output muted | Check ALSA mixer settings |
| High latency | Backbone congestion | Check Guardian availability |

## 7. Next Steps

- Join the community: [lyceum.example.org/community](https://lyceum.example.org/community)
- Report issues: GitHub Issues in this repository
- Contribute enclosures: `/hardware/enclosures/` directory
