# Gateway Module

E22 LoRa driver and Pneuma protocol implementation for The Lyceum.

> **Note:** This module was merged from the standalone `e22-lyceum-gateway` repository.

## Contents

- `lyceum/` - Pneuma protocol package (messages, router, discovery, crypto)
- `e22_driver.py` - E22-900T22U LoRa module driver
- `tests/` - Protocol tests (48 passing)

## Quick Start

```python
# From The-Lyceum root
from gateway import RoutingRequest, IntentClassifier, AESGCMCipher

# Or directly
from gateway.lyceum.pneuma import DebatePacket
```

## Running Tests

```bash
cd gateway
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
PYTHONPATH=. .venv/bin/pytest tests/ -v
```
