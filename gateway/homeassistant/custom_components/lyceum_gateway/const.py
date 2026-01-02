"""Constants for the Lyceum Gateway integration."""

DOMAIN = "lyceum_gateway"

# Config keys
CONF_PORT = "port"
CONF_CHANNEL = "channel"
CONF_AES_KEY = "aes_key"
CONF_NODE_ID = "node_id"
CONF_BACKBONE_MODE = "backbone_mode"
CONF_RELAY_URL = "relay_url"

# Guardian config keys
CONF_GUARDIAN_ENABLED = "guardian_enabled"
CONF_GUARDIAN_SKILLS = "guardian_skills"
CONF_GUARDIAN_CPU_LIMIT = "guardian_cpu_limit"
CONF_GUARDIAN_MEMORY_LIMIT = "guardian_memory_limit"
CONF_GUARDIAN_SYMBOLONS = "guardian_symbolons"
CONF_GUARDIAN_EARN_TOKENS = "guardian_earn_tokens"

# Default values
DEFAULT_CHANNEL = 4
DEFAULT_NODE_ID = "!ha_gateway"
DEFAULT_RELAY_URL = "https://relay.lyceum.example.org"
DEFAULT_GUARDIAN_CPU = 25
DEFAULT_GUARDIAN_MEMORY = 512

# Guardian skills
SKILL_RELAY = "relay"
SKILL_REFLEX_STT = "reflex_stt"
SKILL_REFLEX_TTS = "reflex_tts"
SKILL_CORTEX = "cortex"
SKILL_SYMBOLON = "symbolon"

ALL_SKILLS = [SKILL_RELAY, SKILL_REFLEX_STT, SKILL_REFLEX_TTS, SKILL_CORTEX, SKILL_SYMBOLON]

# Event types
EVENT_MESSAGE_RECEIVED = f"{DOMAIN}_message_received"
EVENT_MESSAGE_SENT = f"{DOMAIN}_message_sent"
EVENT_JOB_COMPLETED = f"{DOMAIN}_job_completed"

# Sensor attributes
ATTR_RSSI = "rssi"
ATTR_SNR = "snr"
ATTR_SENDER = "sender"
ATTR_CHANNEL = "channel"
ATTR_TIMESTAMP = "timestamp"
ATTR_TOKENS_EARNED = "tokens_earned"
ATTR_JOBS_COMPLETED = "jobs_completed"
