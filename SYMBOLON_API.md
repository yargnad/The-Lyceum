# Symbolon API Specification

**Version:** 0.1 - Draft
**Status:** DRAFT - Initial Scaffolding

## 1. Overview

Symbolons are self-contained, containerized applications offered by developers to The Lyceum commons. This document defines the API for creating, registering, and deploying Symbolon apps.

## 2. Symbolon Architecture

```
┌─────────────────────────────────────┐
│         Symbolon Container          │
├─────────────────────────────────────┤
│  ┌─────────────┐  ┌──────────────┐  │
│  │ Application │  │ Lyceum SDK   │  │
│  │   Logic     │◀─│ Integration  │  │
│  └─────────────┘  └──────────────┘  │
├─────────────────────────────────────┤
│  minimal Alpine base + runtime      │
└─────────────────────────────────────┘
           │
           ▼
    ┌─────────────┐
    │   Pneuma    │
    │  Guardian   │
    └─────────────┘
```

## 3. SDK Interface

### 3.1 Python SDK

```python
from lyceum_sdk import Symbolon, PneumaClient

class MyApp(Symbolon):
    """Example Symbolon application."""
    
    name = "my-app"
    version = "1.0.0"
    skills = ["data-analysis", "visualization"]
    
    async def on_request(self, prompt: str, context: dict) -> str:
        """Handle incoming requests."""
        # Process request using Pneuma if needed
        result = await self.pneuma.query(
            prompt=f"Analyze: {prompt}",
            skills=["math", "statistics"],
        )
        return result.text
    
    async def on_install(self):
        """Called when Symbolon is deployed."""
        pass
    
    async def on_uninstall(self):
        """Called when Symbolon is removed."""
        pass
```

### 3.2 Required Methods

| Method | Description | Required |
|--------|-------------|----------|
| `on_request` | Handle incoming user requests | Yes |
| `on_install` | Post-installation setup | No |
| `on_uninstall` | Cleanup before removal | No |
| `on_update` | Handle version upgrades | No |

### 3.3 Metadata Schema

```yaml
# symbolon.yaml
name: my-app
version: 1.0.0
description: Short description of the app
author: developer@example.org

# Skills this Symbolon provides to the network
skills:
  - data-analysis
  - visualization

# Resource requirements
resources:
  memory_mb: 256
  cpu_cores: 0.5
  npu_required: false
  gpu_required: false

# Permissions requested
permissions:
  - network.local    # Access to Layer 2
  - storage.cache    # Temporary file storage
  # - network.wan    # Requires Guardian approval

# Entry point
entrypoint: my_app:MyApp
```

## 4. Registration & Vetting

### 4.1 Registration Flow

1. Developer submits Symbolon to The Agora
2. Automated security scan runs (static analysis)
3. Guardian nodes run benchmark suite
4. If new developer, token stake required
5. Approved Symbolons appear in The Agora

### 4.2 Benchmark Requirements

Symbolons must pass the standard benchmark suite:

```bash
# Run benchmarks locally before submission
lyceum-sdk benchmark ./my-symbolon/

# Benchmark categories:
# - Response latency (p95 < 500ms)
# - Memory footprint (< declared limit)
# - CPU utilization (< declared limit)
# - Security scan (no known vulnerabilities)
```

### 4.3 Staking

New developers stake tokens to discourage malicious apps:

| Reputation | Stake Required |
|------------|----------------|
| New (0-10) | 100 tokens |
| Established (10-50) | 50 tokens |
| Trusted (50+) | 0 tokens |

Stakes are slashed if:

- Security vulnerability discovered
- App exceeds resource limits repeatedly
- Guardian veto by 2+ nodes

## 5. The Agora API

### 5.1 Discovery

```python
# Search available Symbolons
results = await agora.search(
    query="data analysis",
    skills=["visualization"],
    max_results=10,
)

for app in results:
    print(f"{app.name} v{app.version} by {app.author}")
    print(f"  Skills: {app.skills}")
    print(f"  Rating: {app.rating}/5")
```

### 5.2 Installation

```python
# Install on local node
await agora.install("my-app", version="1.0.0")

# List installed Symbolons
installed = await agora.list_installed()
```

### 5.3 Invocation

```python
# Call a Symbolon
response = await pneuma.invoke(
    symbolon="my-app",
    prompt="Analyze this data: [...]",
)
```

## 6. Security Model

### 6.1 Container Sandboxing

- Symbolons run in rootless containers (Podman/Docker)
- Network access limited to declared permissions
- Filesystem access restricted to app directory
- No access to host GPU/NPU without approval

### 6.2 Permission Levels

| Permission | Description | Approval |
|------------|-------------|----------|
| `network.local` | Layer 2 mesh only | Automatic |
| `network.wan` | Layer 3 backbone | Guardian approval |
| `storage.cache` | Temp files in `/tmp` | Automatic |
| `storage.persistent` | Permanent storage | User approval |
| `hardware.npu` | NPU access | Guardian approval |
| `hardware.gpu` | GPU access | Guardian approval |

## 7. Example Symbolons

| Name | Description | Skills |
|------|-------------|--------|
| `lyceum-weather` | Local weather aggregation | `weather`, `sensor-fusion` |
| `lyceum-translate` | Offline translation | `translation`, `language` |
| `lyceum-code` | Code assistance | `code`, `python`, `rust` |
| `lyceum-emergency` | Emergency beacon/alert | `emergency`, `location` |
