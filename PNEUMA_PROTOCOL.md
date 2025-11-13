Pneuma Protocol Specification (v1.0)
Status: Draft Implementation Contract Scope: Defines the JSON wire protocols, transport mechanisms, and handshake logic for the Pneuma Federated Mind.
1. Message Transport Layers
Pneuma operates over two distinct transport layers. The protocol is transport-agnostic but assumes specific constraints for each.
1.1 Layer 2 (Local/LAN) - "The Fast Lane"
Transport: TCP/IP via Wi-Fi HaLow or Standard Wi-Fi.
Protocol: HTTP/2 or gRPC.
Payload Limit: High (MBs allowed).
Use Case: Local routing, Petals-style tensor transfer, rapid debate.
1.2 Layer 3 (Backbone/WAN) - "The Thin Lane"
Transport: LoRa via Meshtastic.
Protocol: Compressed Binary (Protocol Buffers / CBOR) encapsulated in Meshtastic PRIVATE_APP packets.
Payload Limit: ~200-230 bytes per packet (multipart supported but discouraged).
Use Case: Remote expert discovery, text-only debate, final synthesis delivery.
2. JSON Schemas & Message Types
All messages are JSON objects (serialized to CBOR for L3).
2.1 The RoutingRequest (Stage A -> B)
Broadcast by the Moderator to find Experts.
{
  "type": "route_req",
  "id": "req_a1b2_887",       // Unique Request ID
  "timestamp": 1715420000,
  "origin": "!node_a1b2",     // Moderator Node ID
  "intent": {
    "primary": "code",        // Primary Skill Needed
    "secondary": ["security"] // Optional Critiques Needed
  },
  "constraints": {
    "max_latency": 2000,      // Max acceptable RTT in ms
    "min_reputation": 50,     // Minimum Pneuma Vault score
    "cost_cap": 0.5           // Max token cost willing to pay
  },
  "payload_hash": "sha256..." // Hash of the full prompt (for integrity)
}


2.2 The ExpertOffer (Stage B Response)
Sent by a Guardian Node offering its services.
{
  "type": "expert_offer",
  "req_id": "req_a1b2_887",
  "guardian_id": "!node_c3d4",
  "expert_type": "qwen-2.5-coder-7b", // Specific Model hosted
  "capabilities": ["code", "python"],
  "bid": {
    "cost": 0.1,              // Token cost for this job
    "est_latency": 800        // Estimated processing time ms
  },
  "signature": "sig_..."      // Cryptographic proof of identity
}


2.3 The DebatePacket (Stage C Execution)
The core exchange of thought.
{
  "type": "debate",
  "session_id": "sess_998877",
  "round": 1,                 // Round 1 or 2 (Hard cap)
  "role": "proposer",         // "proposer" or "critic"
  "content": "def scan_bt(): ...", // The actual text generation
  "metadata": {
    "confidence": 0.92,
    "citations": []
  }
}


3. The "Stage A" Handshake Logic (The Router)
This is the state machine logic for the Lightweight Moderator (AIWT).
State 1: CLASSIFY
User Input: "Write a secure Python script for..."
Local NPU (TinyBERT/Qwen-3B) runs classification.
Output: intent: code, sensitivity: high.
State 2: DISCOVERY (The "Holler")
Construct RoutingRequest JSON.
Action: Broadcast to Layer 2 (UDP Multicast or HaLow Beacon).
Timer: Start T_DISCOVER (200ms).
State 3: SELECTION (The Auction)
Listen for ExpertOffer messages.
IF T_DISCOVER expires AND offers.count > 0:
Sort offers by: (Reputation * 0.6) + (1/Latency * 0.4).
Select Top 1 Proposer and Top 1 Critic.
Send SessionInit (encrypted with selected Guardians' public keys) containing the full user prompt.
IF T_DISCOVER expires AND offers.count == 0:
Escalate: Re-broadcast RoutingRequest to Layer 3 (Backbone).
Timer: Start T_BACKBONE (2000ms).
State 4: EXECUTION
Receive DebatePacket from Proposer.
Forward payload to Critic (if active).
Receive DebatePacket from Critic.
Synthesis: Local NPU runs fusion/summarization.
Display: Stream result to user.
4. Security & Encryption
Transport Encryption: All L3 packets use Meshtastic's native AES256.
Payload Encryption: The "Full Prompt" in SessionInit and all DebatePacket content fields are encrypted end-to-end using an ephemeral session key derived from the Moderator and Guardian's verified public keys (ECDH). The intermediate relays (L3 nodes) cannot read the debate text.
5. Telemetry Compression (Level 1.5)
For Arduino UNO Q / Hybrid nodes sending sensor data over L3:
Format: Protobuf SensorFrame.
Schema:
message SensorFrame {
  uint32 timestamp = 1;
  uint32 node_id = 2;
  repeated SensorData data = 3;
}
message SensorData {
  enum Type { TEMP=0; HUM=1; RAD=2; SPEC=3; }
  Type type = 1;
  float value = 2;
}


