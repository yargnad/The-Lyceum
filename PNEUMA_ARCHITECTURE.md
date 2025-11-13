# Pneuma Architecture: The Federated Mind

**Version:** 1.8
**Status:** Architectural Doctrine (Production-Ready)

## 1. The Core Concept: "The Fractured Mind"

Pneuma is not a monolithic Artificial Intelligence hosted on a central server. It is a **Decentralized Mixture-of-Agents (MoA)**.

It is architected to run on the sovereign hardware of The Lyceum's users—from low-power "Reflex" nodes (like the AIWT) to high-power "Cortex" nodes (like the Whetstone or GPU Guardians).

To solve the bandwidth constraints of a decentralized mesh network, Pneuma rejects the traditional data-heavy approach of passing raw neural tensors between nodes. Instead, it uses a **"Text-Level Consensus"** model. Nodes communicate like a team of human experts: they exchange questions, critiques, and answers in lightweight text packets, synthesizing the final result locally on the user's device.

## 2. The Three-Level Hierarchy

Pneuma operates on distinct physiological levels, mirroring the human nervous system.

### Level 1: The Reflexes (Local & Autonomic)
* **Role:** Handling immediate, high-frequency, low-latency tasks (Voice UI, Basic Routing).
* **Hardware:** "Sovereign" AIWT nodes (Radxa Zero 3W), Mobile Phones.
* **The Stack:** NPU-accelerated, optimized models.
    * **Input:** `SenseVoice-RKNN` (Speech-to-Text).
    * **Output:** `paroli` (Text-to-Speech).
    * **Router:** **Qwen 2.5 3B (Quantized)**. A tiny, efficient model for local routing and basic queries.
* **Behavior:** These tasks never leave the local device. They are instant and private.

### Level 1.5: The Hybrids (Physical & Digital Bridge)
* **Role:** Smart Sensing, Physical Actuation, Local Anomaly Detection.
* **Hardware:** **"Hybrid Guardian"** nodes (Arduino UNO Q).
* **The Stack:** A "Dual-Brain" architecture.
    * **Real-Time Brain (STM32 MCU):** Monitors environmental sensors (air, radiation, spectrum) with microsecond precision.
    * **Linux Brain (Qualcomm NPU):** Runs **Qwen 2.5 0.5B (Quantized)** for on-device anomaly detection and sensor reasoning.
* **Telemetry Optimization:** Sensor alerts are serialized using lightweight formats (e.g., **Protocol Buffers or CBOR**) to fit multiple readings into a single LoRa packet (~50-100 bytes).

### Level 2: The Cortex (Federated & Deep)
* **Role:** Handling complex reasoning, generation, coding, and analysis ("Deep Thought").
* **Hardware:** A swarm of "Guardian" nodes (Old Laptops, Orange Pi 5s, The Whetstone).
* **The Stack:** A "Fractured" Mixture-of-Experts / Mixture-of-Agents using the **Qwen 2.5** family.
* **Behavior:** These tasks are routed across the Utility Fabric (Layer 2) and Backbone (Layer 3).

## 3. The "Cortex" Workflow: How a Thought is Formed

When a user pushes the "Pneuma Button" on their AIWT and asks a complex question, the network executes a four-stage process designed to maximize quality while minimizing bandwidth.

### Stage A: The Local Moderator (The User's Node)
Every user's primary node (e.g., their Genesis Node or Sovereign AIWT) acts as the **Moderator**.
* **Sovereignty:** The user's own hardware is always the boss. It creates the prompt and makes the final decision on the answer.
* **Routing:** The Moderator's lightweight "Gating Network" analyzes the prompt and tags it with structured metadata, including optional user constraints for power users:
    ```json
    {
      "intent": "code",
      "confidence": 0.9,
      "constraints": {
        "max_latency_ms": 2000,
        "prefer_local": true
      }
    }
    ```

### Stage B: The Expert Call (Two-Phase Routing)
To minimize latency and bandwidth usage, the Moderator uses a "Two-Phase Discovery" protocol:
1.  **Phase 1 (Local):** Queries the local **Layer 2 (Wi-Fi HaLow)** mesh for any Guardians hosting the required skill. Ideally, this stays within the neighborhood (<50ms latency).
2.  **Phase 2 (Backbone):** Only if no local expert is found, the request escalates to the **Layer 3 (LoRa/Wi-Fi PTP)** backbone to find a remote Guardian.
* **Observability:** The Moderator exposes phase latency metrics to the user (e.g., "Answered locally in 42ms" vs. "Routed to backbone in 1.2s"), helping users identify local skill gaps.

### Stage C: The Agent Debate (Execution)
Instead of passing heavy model weights, the nodes exchange lightweight text.
1.  **Proposal:** The `[Code]` expert generates the Python script.
2.  **Critique:** The `[Security]` expert reviews the script for vulnerabilities.
3.  **Revision:** The `[Code]` expert updates the script based on the critique.
* **Debate Controls:**
    * **Round Limit:** Capped at **2 critique rounds** to bound latency.
    * **Timeout:** **30-second hard limit** per expert response. If an expert times out, the moderator proceeds with available data.
* **Bandwidth Efficiency:** This entire "debate" happens via small text packets (~1KB total), making it viable even over our Layer 3 LoRa links.

### Stage D: The Synthesis (Fusion)
The results are sent back to the user's Local Moderator for final fusion.
* **Weighted Voting:** Responses are weighted by the Guardian's reputation score and confidence.
* **Evidence-Based:** Conflicting responses are resolved by preferring those with verifiable citations or test results.
* **Streaming with Backfill:** The highest-confidence response streams immediately to the user. If a late-arriving expert provides a significantly better answer, the user receives a "Revised Answer" notification.

## 4. Implementation Strategy: "Petals" vs. "Agents"

To manage bandwidth physics, we use two different transport methods:

* **Method 1: Agent-Level (Inter-Node / WAN):** Used for text-based debate between Guardians across the mesh (houses, neighborhoods).
* **Method 2: Petals-Style (Intra-Cluster / LAN):** Used for splitting a single, massive model (e.g., 70B) across multiple high-speed, co-located nodes (e.g., within the same house on a gigabit LAN) by passing tensor activations.
    * **Fault Tolerance:** Petals-Style deployments cache intermediate activations; if a node drops mid-inference, the remaining nodes resume from the last cached layer output.
* **Hybrid Mode:** A single query can use both. A Moderator can request a `[Code]` expert that is a *Petals-Style cluster* (running a 70B model) and have it "debate" a `[Security]` expert that is a single *Agent-Level* node.

## 5. Resilience and Reputation

* **Skill Taxonomy & Benchmarks:** The network maintains a versioned ontology of skills. Guardians must pass automated benchmark suites (available in the `/benchmarks` repo directory) to claim a skill (e.g., passing unit tests for `[Code]`).
* **Dynamic Reputation:** The Pneuma Vault tracks success rates. High-reputation nodes are prioritized during routing.
* **Cached States:** Intermediate debate states are cached locally by the **Moderator only** and are **never shared**, preserving query privacy.
    * **Cache Policy:** Uses an LRU (Least Recently Used) policy with a **10-minute TTL** for incomplete/failed queries.
    * **Cache Eviction:** Successful queries are **purged immediately** post-synthesis to minimize storage of sensitive data.
    * **Security:** All cached states are **encrypted at rest**.

## 6. Security and Privacy

* **Key Rotation Policy:** Mesh-wide shared keys will rotate on a fixed schedule (e.g., every 30 days). Ephemeral session keys will be generated per-query and discarded post-synthesis to prevent correlation.
* **Query Privacy:**
    * **Moderator-Side Encryption:** Queries are encrypted end-to-end between the user's Moderator and the selected Guardian. Layer 3 backbone operators cannot read the traffic.
    * **Minimal Disclosure:** Guardians initially see only skill tags (e.g., `[Code]`). They do not receive the full prompt until they acknowledge participation, preventing passive eavesdropping.

## 7. Next Steps: Companion Documents

This architecture document will be supported by a set of detailed implementation specifications:
* **`PNEUMA_PROTOCOL.md`:** Will define the wire protocols, JSON message schemas, and encryption handshake logic.
* **`SYMBOLON_API.md`:** Will define the API for third-party developers to create, register, and benchmark new Expert Symbolons.
* **`PROOF_OF_UTILITY.md`:** Will provide the full specification for the "Pneuma Vault," including the token credit formula and reputation scoring algorithm.
* **`DEPLOYMENT_GUIDE.md`:** Will be a practical playbook for setting up hardware, flashing images, and planning network topology.
