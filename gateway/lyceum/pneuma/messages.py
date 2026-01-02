"""
Pneuma Protocol Message Types

Implements the JSON schemas defined in PNEUMA_PROTOCOL.md:
- RoutingRequest (Stage A → B): Moderator broadcasts to find Experts
- ExpertOffer (Stage B Response): Guardian offers its services
- DebatePacket (Stage C Execution): Core exchange of thought

All messages serialize to JSON for Layer 2 (TCP/IP) or CBOR for Layer 3 (LoRa).
"""
from dataclasses import dataclass, field, asdict
from typing import Optional, List, Dict, Any
import json
import time
import hashlib


@dataclass
class IntentConstraints:
    """Optional user constraints for power users."""
    max_latency_ms: int = 2000
    min_reputation: int = 50
    cost_cap: float = 0.5
    prefer_local: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "max_latency": self.max_latency_ms,
            "min_reputation": self.min_reputation,
            "cost_cap": self.cost_cap,
            "prefer_local": self.prefer_local,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "IntentConstraints":
        return cls(
            max_latency_ms=d.get("max_latency", 2000),
            min_reputation=d.get("min_reputation", 50),
            cost_cap=d.get("cost_cap", 0.5),
            prefer_local=d.get("prefer_local", True),
        )


@dataclass
class Intent:
    """Structured metadata from the Gating Network."""
    primary: str  # e.g., "code", "security", "general"
    secondary: List[str] = field(default_factory=list)
    confidence: float = 0.9

    def to_dict(self) -> Dict[str, Any]:
        return {
            "primary": self.primary,
            "secondary": self.secondary,
            "confidence": self.confidence,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "Intent":
        return cls(
            primary=d["primary"],
            secondary=d.get("secondary", []),
            confidence=d.get("confidence", 0.9),
        )


@dataclass
class RoutingRequest:
    """
    Stage A → B: Broadcast by the Moderator to find Experts.
    
    The Moderator's lightweight "Gating Network" analyzes the prompt
    and tags it with structured metadata.
    """
    id: str
    origin: str  # Moderator Node ID, e.g., "!node_a1b2"
    intent: Intent
    constraints: IntentConstraints = field(default_factory=IntentConstraints)
    timestamp: int = field(default_factory=lambda: int(time.time()))
    payload_hash: str = ""  # SHA256 of the full prompt

    MSG_TYPE = "route_req"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.MSG_TYPE,
            "id": self.id,
            "timestamp": self.timestamp,
            "origin": self.origin,
            "intent": self.intent.to_dict(),
            "constraints": self.constraints.to_dict(),
            "payload_hash": self.payload_hash,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "RoutingRequest":
        return cls(
            id=d["id"],
            origin=d["origin"],
            intent=Intent.from_dict(d["intent"]),
            constraints=IntentConstraints.from_dict(d.get("constraints", {})),
            timestamp=d.get("timestamp", int(time.time())),
            payload_hash=d.get("payload_hash", ""),
        )

    @classmethod
    def from_json(cls, s: str) -> "RoutingRequest":
        return cls.from_dict(json.loads(s))

    @staticmethod
    def hash_payload(payload: str) -> str:
        """Generate SHA256 hash of the full prompt for integrity."""
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()


@dataclass
class Bid:
    """Guardian's cost and latency estimate for a job."""
    cost: float  # Token cost
    est_latency_ms: int  # Estimated processing time

    def to_dict(self) -> Dict[str, Any]:
        return {
            "cost": self.cost,
            "est_latency": self.est_latency_ms,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "Bid":
        return cls(
            cost=d["cost"],
            est_latency_ms=d["est_latency"],
        )


@dataclass
class ExpertOffer:
    """
    Stage B Response: Sent by a Guardian Node offering its services.
    
    Guardians respond to RoutingRequests with their capabilities and bids.
    """
    req_id: str  # The original RoutingRequest ID
    guardian_id: str  # e.g., "!node_c3d4"
    expert_type: str  # e.g., "qwen-2.5-coder-7b"
    capabilities: List[str]  # e.g., ["code", "python"]
    bid: Bid
    signature: str = ""  # Cryptographic proof of identity

    MSG_TYPE = "expert_offer"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.MSG_TYPE,
            "req_id": self.req_id,
            "guardian_id": self.guardian_id,
            "expert_type": self.expert_type,
            "capabilities": self.capabilities,
            "bid": self.bid.to_dict(),
            "signature": self.signature,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ExpertOffer":
        return cls(
            req_id=d["req_id"],
            guardian_id=d["guardian_id"],
            expert_type=d["expert_type"],
            capabilities=d["capabilities"],
            bid=Bid.from_dict(d["bid"]),
            signature=d.get("signature", ""),
        )

    @classmethod
    def from_json(cls, s: str) -> "ExpertOffer":
        return cls.from_dict(json.loads(s))


@dataclass
class DebateMetadata:
    """Metadata attached to debate content."""
    confidence: float = 0.9
    citations: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "confidence": self.confidence,
            "citations": self.citations,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "DebateMetadata":
        return cls(
            confidence=d.get("confidence", 0.9),
            citations=d.get("citations", []),
        )


@dataclass
class DebatePacket:
    """
    Stage C Execution: The core exchange of thought.
    
    Nodes exchange lightweight text via proposals and critiques.
    Protocol caps debates at 2 critique rounds with 30-second timeout.
    """
    session_id: str
    round: int  # 1 or 2 (hard cap)
    role: str  # "proposer" or "critic"
    content: str  # The actual text generation
    metadata: DebateMetadata = field(default_factory=DebateMetadata)

    MSG_TYPE = "debate"

    # Protocol constants from PNEUMA_ARCHITECTURE.md
    MAX_ROUNDS = 2
    TIMEOUT_SECONDS = 30

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.MSG_TYPE,
            "session_id": self.session_id,
            "round": self.round,
            "role": self.role,
            "content": self.content,
            "metadata": self.metadata.to_dict(),
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "DebatePacket":
        return cls(
            session_id=d["session_id"],
            round=d["round"],
            role=d["role"],
            content=d["content"],
            metadata=DebateMetadata.from_dict(d.get("metadata", {})),
        )

    @classmethod
    def from_json(cls, s: str) -> "DebatePacket":
        return cls.from_dict(json.loads(s))

    def is_valid_round(self) -> bool:
        """Check if round number is within protocol limits."""
        return 1 <= self.round <= self.MAX_ROUNDS

    def is_proposer(self) -> bool:
        return self.role == "proposer"

    def is_critic(self) -> bool:
        return self.role == "critic"


def parse_message(data: str) -> Optional[Any]:
    """
    Parse a JSON message and return the appropriate message type.
    Returns None if parsing fails or message type is unknown.
    """
    try:
        d = json.loads(data)
        msg_type = d.get("type")
        if msg_type == RoutingRequest.MSG_TYPE:
            return RoutingRequest.from_dict(d)
        elif msg_type == ExpertOffer.MSG_TYPE:
            return ExpertOffer.from_dict(d)
        elif msg_type == DebatePacket.MSG_TYPE:
            return DebatePacket.from_dict(d)
        return None
    except (json.JSONDecodeError, KeyError, TypeError):
        return None
