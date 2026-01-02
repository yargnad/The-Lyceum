"""Tests for Pneuma protocol message types."""
import pytest
import json
from lyceum.pneuma.messages import (
    RoutingRequest,
    ExpertOffer,
    DebatePacket,
    Intent,
    IntentConstraints,
    Bid,
    DebateMetadata,
    parse_message,
)


class TestIntent:
    def test_to_dict(self):
        intent = Intent(primary="code", secondary=["security"], confidence=0.95)
        d = intent.to_dict()
        assert d["primary"] == "code"
        assert d["secondary"] == ["security"]
        assert d["confidence"] == 0.95

    def test_from_dict(self):
        d = {"primary": "math", "secondary": ["general"]}
        intent = Intent.from_dict(d)
        assert intent.primary == "math"
        assert intent.secondary == ["general"]
        assert intent.confidence == 0.9  # Default


class TestRoutingRequest:
    def test_roundtrip_json(self):
        req = RoutingRequest(
            id="req_test_001",
            origin="!node_a1b2",
            intent=Intent(primary="code", secondary=["security"]),
            constraints=IntentConstraints(max_latency_ms=1000),
        )
        
        json_str = req.to_json()
        parsed = RoutingRequest.from_json(json_str)
        
        assert parsed.id == req.id
        assert parsed.origin == req.origin
        assert parsed.intent.primary == req.intent.primary
        assert parsed.constraints.max_latency_ms == 1000

    def test_hash_payload(self):
        hash1 = RoutingRequest.hash_payload("test prompt")
        hash2 = RoutingRequest.hash_payload("test prompt")
        hash3 = RoutingRequest.hash_payload("different prompt")
        
        assert hash1 == hash2
        assert hash1 != hash3
        assert len(hash1) == 64  # SHA256 hex

    def test_msg_type(self):
        req = RoutingRequest(
            id="req_001",
            origin="!node_test",
            intent=Intent(primary="general"),
        )
        d = req.to_dict()
        assert d["type"] == "route_req"


class TestExpertOffer:
    def test_roundtrip_json(self):
        offer = ExpertOffer(
            req_id="req_test_001",
            guardian_id="!node_c3d4",
            expert_type="qwen-2.5-coder-7b",
            capabilities=["code", "python"],
            bid=Bid(cost=0.1, est_latency_ms=800),
            signature="sig_test",
        )
        
        json_str = offer.to_json()
        parsed = ExpertOffer.from_json(json_str)
        
        assert parsed.req_id == offer.req_id
        assert parsed.guardian_id == offer.guardian_id
        assert parsed.capabilities == ["code", "python"]
        assert parsed.bid.cost == 0.1
        assert parsed.bid.est_latency_ms == 800

    def test_msg_type(self):
        offer = ExpertOffer(
            req_id="req_001",
            guardian_id="!node_test",
            expert_type="test-model",
            capabilities=["general"],
            bid=Bid(cost=0.1, est_latency_ms=500),
        )
        d = offer.to_dict()
        assert d["type"] == "expert_offer"


class TestDebatePacket:
    def test_roundtrip_json(self):
        packet = DebatePacket(
            session_id="sess_001",
            round=1,
            role="proposer",
            content="def scan_bt(): ...",
            metadata=DebateMetadata(confidence=0.92, citations=["RFC 1234"]),
        )
        
        json_str = packet.to_json()
        parsed = DebatePacket.from_json(json_str)
        
        assert parsed.session_id == packet.session_id
        assert parsed.round == 1
        assert parsed.role == "proposer"
        assert parsed.content == "def scan_bt(): ..."
        assert parsed.metadata.confidence == 0.92
        assert parsed.metadata.citations == ["RFC 1234"]

    def test_valid_round(self):
        p1 = DebatePacket(session_id="s1", round=1, role="proposer", content="")
        p2 = DebatePacket(session_id="s1", round=2, role="critic", content="")
        p3 = DebatePacket(session_id="s1", round=3, role="proposer", content="")
        
        assert p1.is_valid_round() is True
        assert p2.is_valid_round() is True
        assert p3.is_valid_round() is False  # Exceeds MAX_ROUNDS

    def test_role_helpers(self):
        proposer = DebatePacket(session_id="s", round=1, role="proposer", content="")
        critic = DebatePacket(session_id="s", round=1, role="critic", content="")
        
        assert proposer.is_proposer() is True
        assert proposer.is_critic() is False
        assert critic.is_proposer() is False
        assert critic.is_critic() is True

    def test_msg_type(self):
        packet = DebatePacket(session_id="s", round=1, role="proposer", content="test")
        d = packet.to_dict()
        assert d["type"] == "debate"


class TestParseMessage:
    def test_parse_routing_request(self):
        data = json.dumps({
            "type": "route_req",
            "id": "req_001",
            "origin": "!node_a",
            "intent": {"primary": "code"},
            "timestamp": 1234567890,
        })
        msg = parse_message(data)
        assert isinstance(msg, RoutingRequest)
        assert msg.id == "req_001"

    def test_parse_expert_offer(self):
        data = json.dumps({
            "type": "expert_offer",
            "req_id": "req_001",
            "guardian_id": "!node_b",
            "expert_type": "test-model",
            "capabilities": ["code"],
            "bid": {"cost": 0.1, "est_latency": 500},
        })
        msg = parse_message(data)
        assert isinstance(msg, ExpertOffer)
        assert msg.guardian_id == "!node_b"

    def test_parse_debate_packet(self):
        data = json.dumps({
            "type": "debate",
            "session_id": "sess_001",
            "round": 1,
            "role": "proposer",
            "content": "test content",
        })
        msg = parse_message(data)
        assert isinstance(msg, DebatePacket)
        assert msg.content == "test content"

    def test_parse_unknown_type(self):
        data = json.dumps({"type": "unknown", "data": "test"})
        msg = parse_message(data)
        assert msg is None

    def test_parse_invalid_json(self):
        msg = parse_message("not valid json")
        assert msg is None
