# Lyceum Gateway - Home Assistant Integration

This custom component allows you to use an E22-900T22U USB LoRa module as a Lyceum network gateway directly from Home Assistant.

## Why Home Assistant?

During The Lyceum's bootstrapping phase, mesh coverage may be limited. By running the gateway on Home Assistant:

1. **24/7 Operation** - HA servers run continuously
2. **Internet Backhaul** - Relay messages between distant nodes via your home internet
3. **Automation** - Trigger actions based on Lyceum messages
4. **Ubiquity** - Millions of HA installations worldwide

## Installation

1. Copy the `custom_components/lyceum_gateway` folder to your HA `config/custom_components/` directory:

```bash
cp -r custom_components/lyceum_gateway /path/to/homeassistant/config/custom_components/
```

1. Restart Home Assistant

2. Go to **Settings → Devices & Services → Add Integration → Lyceum Gateway**

3. Select your E22 USB serial port and configure options

## Configuration Options

| Option | Description |
|--------|-------------|
| Serial Port | USB serial device (e.g., `/dev/ttyUSB0`) |
| Channel | LoRa channel 0-83 (default: 4) |
| Node ID | Your gateway's mesh address (e.g., `!ha_gateway`) |
| AES Key | Optional AES-128/256 encryption key (hex) |
| Backbone Mode | Enable internet relay for distant nodes |
| Relay URL | Backbone relay server URL |

## Entities

| Entity | Type | Description |
|--------|------|-------------|
| `sensor.lyceum_gateway_last_message` | Sensor | Last received message |
| `sensor.lyceum_gateway_message_count` | Sensor | Total messages received |
| `sensor.lyceum_gateway_signal_strength` | Sensor | RSSI of last message |
| `binary_sensor.lyceum_gateway_connected` | Binary Sensor | Connection status |

## Services

### `lyceum_gateway.send_message`

Send a message over the LoRa mesh.

```yaml
service: lyceum_gateway.send_message
data:
  message: "Hello from HA!"
  destination: 0x1234  # Or 0xFFFF for broadcast
  channel: 4
```

### `lyceum_gateway.relay_to_internet`

Forward a message via internet backbone (for bootstrapping).

```yaml
service: lyceum_gateway.relay_to_internet
data:
  message: "Long distance relay"
```

## Events

The integration fires events for automation triggers:

- `lyceum_gateway_message_received` - New message arrived
- `lyceum_gateway_message_sent` - Message successfully sent

### Example Automation

```yaml
automation:
  - alias: "Announce Lyceum Messages"
    trigger:
      - platform: event
        event_type: lyceum_gateway_message_received
    action:
      - service: tts.speak
        data:
          message: "Lyceum message: {{ trigger.event.data.message }}"
```

## Backbone Mode

When **Backbone Mode** is enabled, the gateway can relay messages between mesh nodes that are too far apart for direct LoRa communication.

---

## Guardian Mode (Optional)

Enable **Guardian Mode** to contribute your HA server's compute resources to the Pneuma network:

| Setting | Description |
|---------|-------------|
| Guardian Enabled | Turn on compute contribution |
| Skills | What to contribute: `relay`, `reflex_stt`, `reflex_tts`, `cortex`, `symbolon` |
| CPU Limit | Max CPU % for jobs (default: 25%) |
| Memory Limit | Max RAM in MB (default: 512) |
| Symbolons | List of approved apps to host |
| Earn Tokens | Participate in Proof-of-Utility |

### Guardian Entities

| Entity | Description |
|--------|-------------|
| `sensor.lyceum_guardian_tokens_earned` | Tokens earned from compute jobs |
| `sensor.lyceum_guardian_jobs_completed` | Total jobs processed |

### Guardian Services

```yaml
# Get Guardian stats
service: lyceum_gateway.guardian_stats

# Start a Symbolon
service: lyceum_gateway.start_symbolon
data:
  name: "lyceum-weather"

# Stop a Symbolon
service: lyceum_gateway.stop_symbolon
data:
  name: "lyceum-weather"
```
