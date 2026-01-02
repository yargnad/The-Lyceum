"""Constants for the Lyceum Gateway integration."""

DOMAIN = "lyceum_gateway"

# Config keys
CONF_PORT = "port"
CONF_CHANNEL = "channel"
CONF_AES_KEY = "aes_key"
CONF_NODE_ID = "node_id"
CONF_BACKBONE_MODE = "backbone_mode"
CONF_RELAY_URL = "relay_url"

# Default values
DEFAULT_CHANNEL = 4
DEFAULT_NODE_ID = "!ha_gateway"
DEFAULT_RELAY_URL = "https://relay.lyceum.example.org"

# Event types
EVENT_MESSAGE_RECEIVED = f"{DOMAIN}_message_received"
EVENT_MESSAGE_SENT = f"{DOMAIN}_message_sent"

# Sensor attributes
ATTR_RSSI = "rssi"
ATTR_SNR = "snr"
ATTR_SENDER = "sender"
ATTR_CHANNEL = "channel"
ATTR_TIMESTAMP = "timestamp"
