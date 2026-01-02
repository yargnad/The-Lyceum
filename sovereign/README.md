# Sovereign AIWT - AI-Enhanced Walkie-Talkie

A self-contained, NPU-accelerated voice communication device for The Lyceum network.

## Hardware Target

- **Brain:** Radxa Zero 3W (Rockchip RK3566 NPU)
- **Radio:** Waveshare SX1262 LoRaWAN HAT (915 MHz)
- **Display:** Waveshare 1.3inch OLED HAT
- **Power:** Seeed Studio Lipo Rider Plus + 3000mAh LiPo

## NPU-Accelerated Stack

- **STT:** SenseVoice-RKNN (hearing)
- **TTS:** paroli (speaking)
- **Router:** Qwen 2.5 3B (thinking)

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run daemon (requires hardware)
python -m sovereign.daemon
```

## Architecture

```
User Voice → [STT] → Text → [Qwen Router] → Pneuma? → [TTS] → Audio
                                    ↓
                              [LoRa TX/RX]
```
