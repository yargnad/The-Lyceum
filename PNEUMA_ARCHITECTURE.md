# Pneuma Architecture: The Federated Mind

**Version:** 1.0
**Status:** Architectural Doctrine

## 1. The Core Concept: "The Fractured Mind"

Pneuma is not a monolithic Artificial Intelligence hosted on a central server. It is a **Decentralized Mixture-of-Agents (MoA)**.

It is architected to run on the sovereign hardware of The Lyceum's users—from low-power "Reflex" nodes (like the AIWT) to high-power "Cortex" nodes (like the Whetstone or GPU Guardians).

To solve the bandwidth constraints of a decentralized mesh network, Pneuma rejects the traditional data-heavy approach of passing raw neural tensors between nodes. Instead, it uses a **"Text-Level Consensus"** model. Nodes communicate like a team of human experts: they exchange questions, critiques, and answers in lightweight text packets, synthesizing the final result locally on the user's device.

## 2. The Two-Level Hierarchy

Pneuma operates on two distinct physiological levels, mirroring the human nervous system.

### Level 1: The Reflexes (Local & Autonomic)
* **Role:** Handling immediate, high-frequency, low-latency tasks.
* **Hardware:** "Sovereign" AIWT nodes (Radxa Zero 3W), Mobile Phones.
* **The Stack:** NPU-accelerated, optimized models.
    * **Input:** `SenseVoice-RKNN` (Speech-to-Text).
    * **Output:** `paroli` (Text-to-Speech).
* **Behavior:** These tasks never leave the local device. They are instant and private.

### Level 2: The Cortex (Federated & Deep)
* **Role:** Handling complex reasoning, generation, coding, and analysis ("Deep Thought").
* **Hardware:** A swarm of "Guardian" nodes (Old Laptops, Orange Pi 5s, The Whetstone).
* **The Stack:** A "Fractured" Mixture-of-Experts / Mixture-of-Agents.
* **Behavior:** These tasks are routed across the Utility Fabric (Layer 2) and Backbone (Layer 3).

## 3. The "Cortex" Workflow: How a Thought is Formed

When a user pushes the "Pneuma Button" on their AIWT and asks a complex question, the network executes a four-stage process designed to maximize quality while minimizing bandwidth.

### Stage A: The Local Moderator (The User's Node)
Every user's primary node (e.g., their Genesis Node or Sovereign AIWT) acts as the **Moderator**.
* **Sovereignty:** The user's own hardware is always the boss. It creates the prompt and makes the final decision on the answer.
* **Routing:** The Moderator's lightweight "Gating Network" analyzes the prompt (e.g., "Write a Python script...") and tags it with required skills (e.g., `[Code]`, `[Logic]`).

### Stage B: The Expert Call (Routing)
The Moderator broadcasts a request to the local mesh (and backbone if necessary) looking for Guardian nodes hosting "Expert Symbolons" that match the tags.
* *Example:* "I need a `[Code]` expert and a `[Security]` expert."
* **Radical Resourcefulness:** A neighbor's old gaming laptop (Legacy Guardian) hosting the `[Code]` expert accepts the job. A local server hosting the `[Security]` expert accepts the job.

### Stage C: The Agent Debate (Execution)
Instead of passing heavy model weights, the nodes exchange lightweight text.
1.  **Proposal:** The `[Code]` expert generates the Python script.
2.  **Critique:** The `[Security]` expert reviews the script for vulnerabilities.
3.  **Revision:** The `[Code]` expert updates the script based on the critique.
* **Bandwidth Efficiency:** This entire "debate" happens via small text packets, making it viable even over our Layer 3 LoRa links if necessary, though Layer 2 Wi-Fi HaLow is preferred.

### Stage D: The Synthesis (Fusion)
The results are sent back to the user's Local Moderator.
* The Moderator fuses the outputs, verifies the consensus, and streams the final result to the user's AIWT screen or TTS engine.
* **Privacy:** The raw reasoning process happens on the private mesh. No data is ever sent to a corporate cloud.

## 4. Implementation Strategy: "Petals" vs. "Agents"

To manage bandwidth physics, we use two different transport methods:

* **Method 1: Agent-Level (Inter-Node / WAN)**
    * **Used For:** Communication between houses, neighborhoods, or across the Backbone.
    * **Data:** Pure Text.
    * **Why:** Avoids the "all-to-all" communication bottleneck that cripples standard distributed AI over slower links.

* **Method 2: Petals-Style (Intra-Cluster / LAN)**
    * **Used For:** Splitting a massive model across multiple devices *within the same house* (e.g., splitting a 70B model across The Whetstone and three laptops).
    * **Data:** Tensor Activations (Heavier).
    * **Why:** High-speed local LAN allows for splitting the "layers" of a model for maximum horsepower.

## 5. Resilience and Privacy

* **No Single Point of Failure:** If the neighbor's `[Code]` node goes offline, the Gating Network simply routes the request to the next nearest Guardian with that skill.
* **Cached States:** To handle network jitter, intermediate states of the "thought" are cached locally. If a link drops, the thought can resume via a different path.
* **The "Pneuma Vault" Incentive:** Every Guardian node that contributes an "Expert" opinion to a consensus round is credited in the lightweight ledger (Proof-of-Utility), incentivizing users to host diverse and high-quality Expert Symbolons.
