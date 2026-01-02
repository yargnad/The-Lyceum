# Proof-of-Utility Specification

**Version:** 0.1 - Draft
**Status:** DRAFT - Initial Scaffolding

## 1. Overview

The Lyceum uses a "Proof-of-Utility" model instead of Proof-of-Work or Proof-of-Stake. Tokens are earned as direct receipts for providing verifiable, useful work to the commons.

This document specifies the Pneuma Vault ledger, token credit formula, and reputation scoring algorithm.

## 2. Core Principles

> **"People Over Tokens"** - The token exists to incentivize participation and police bad actors, not as a speculative asset.

1. Tokens are **earned**, not mined
2. The resource cost of tokenization is near-zero
3. NPU/GPU resources are never wasted on bookkeeping
4. Using your own nodes is always free

## 3. The Pneuma Vault

### 3.1 Ledger Structure

The Pneuma Vault is a lightweight, replicated database (not a blockchain):

```
┌─────────────────────────────────────────────┐
│              PNEUMA VAULT                    │
├─────────────────────────────────────────────┤
│  node_id    │ balance │ reputation │ stakes │
├─────────────┼─────────┼────────────┼────────┤
│ !node_a1b2  │  42.5   │    75      │  0.0   │
│ !node_c3d4  │ 128.0   │    92      │ 50.0   │
│ ...         │  ...    │   ...      │  ...   │
└─────────────────────────────────────────────┘
```

### 3.2 Transaction Log

All credit/debit events are logged:

```json
{
  "tx_id": "tx_00001234",
  "timestamp": 1715420000,
  "type": "credit",
  "node_id": "!node_a1b2",
  "amount": 0.1,
  "job_id": "job_5879",
  "job_type": "reflex_stt",
  "verified_by": "!node_c3d4"
}
```

### 3.3 Replication

- Vault state syncs over Layer 3 backbone
- Uses CRDTs for eventual consistency
- Conflict resolution: highest timestamp wins
- Sync interval: every 60 seconds or on backbone connection

## 4. Token Credit Formula

### 4.1 Base Rates

| Job Type | Base Credit | Description |
|----------|-------------|-------------|
| Reflex STT | 0.05 | Speech-to-Text conversion |
| Reflex TTS | 0.03 | Text-to-Speech synthesis |
| Reflex Route | 0.01 | Local intent classification |
| Cortex Query | 0.10 | Federated LLM inference |
| Cortex Code | 0.15 | Code generation/analysis |
| Cortex Debate | 0.05 | Per-round expert debate |
| Relay L3 | 0.02 | Backbone packet forwarding |
| Storage Sym | 0.01/hr | Symbolon hosting |

### 4.2 Modifiers

Credits are adjusted based on:

```
final_credit = base_credit × quality_modifier × scarcity_modifier

quality_modifier = 0.5 + (0.5 × user_rating)  # Range: 0.5 - 1.0
scarcity_modifier = 1.0 + (0.5 × skill_demand)  # Range: 1.0 - 1.5
```

### 4.3 Example Calculation

```
Job: Cortex Code (Python security audit)
Base: 0.15 tokens
User rating: 4/5 → quality = 0.5 + (0.5 × 0.8) = 0.9
Skill demand: 0.6 (security skills in demand) → scarcity = 1.3

Final: 0.15 × 0.9 × 1.3 = 0.1755 tokens
```

## 5. Reputation System

### 5.1 Reputation Score

Each node has a reputation score (0-100):

```
reputation = (success_rate × 40) + (uptime × 30) + (age × 20) + (stake × 10)

success_rate = completed_jobs / total_jobs  # 0.0 - 1.0
uptime = hours_online_30d / (30 × 24)        # 0.0 - 1.0
age = min(months_active / 12, 1.0)           # 0.0 - 1.0
stake = min(staked_tokens / 100, 1.0)        # 0.0 - 1.0
```

### 5.2 Reputation Effects

| Score Range | Effects |
|-------------|---------|
| 0-20 | Limited to Reflex jobs only |
| 20-50 | Standard access, normal routing priority |
| 50-80 | Priority routing, Cortex job access |
| 80-100 | Guardian status, vetting rights |

### 5.3 Reputation Changes

| Event | Change |
|-------|--------|
| Successful job completion | +0.1 |
| User 5-star rating | +0.5 |
| User 1-star rating | -1.0 |
| Job timeout/failure | -0.5 |
| Security violation | -20.0 |
| Guardian veto | -10.0 |

## 6. Spending & Burning

### 6.1 Service Costs

| Service | Cost |
|---------|------|
| Cortex query (non-local) | 0.05 |
| Symbolon invocation | App-defined (0.01-0.10) |
| Priority routing | 0.02 |
| Backbone relay | 0.01 |

### 6.2 Token Burning

Tokens are burned (permanently destroyed) when:

- Developer stake slashed for malicious app
- Spam prevention penalties
- Optional: voluntary donation to commons

### 6.3 The Homestead Principle

**Using your own hardware is always free:**

- Local STT/TTS on your Sovereign: 0 cost
- Queries answered by your own Guardian: 0 cost
- Relaying through your own backbone node: 0 cost

## 7. Implementation Notes

### 7.1 Vault Database

SQLite with custom sync layer:

```sql
CREATE TABLE nodes (
    node_id TEXT PRIMARY KEY,
    balance REAL DEFAULT 0,
    reputation INTEGER DEFAULT 50,
    staked REAL DEFAULT 0,
    created_at INTEGER,
    last_seen INTEGER
);

CREATE TABLE transactions (
    tx_id TEXT PRIMARY KEY,
    timestamp INTEGER,
    type TEXT,  -- 'credit', 'debit', 'stake', 'slash'
    node_id TEXT,
    amount REAL,
    job_id TEXT,
    verified_by TEXT
);
```

### 7.2 Verification

Jobs are verified locally by the requesting node or a nearby Guardian:

1. User's node receives job result
2. Basic validation (response format, timing)
3. Optional: cryptographic proof of compute
4. Credit issued upon verification

### 7.3 Anti-Gaming

Defenses against token farming:

- Rate limiting per node (max 100 jobs/hour)
- Proof of unique hardware (device fingerprinting)
- Guardian auditing of suspicious patterns
- Stake requirements for high-volume activity
