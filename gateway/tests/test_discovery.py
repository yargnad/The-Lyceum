"""Tests for expert discovery protocol."""
import pytest
from lyceum.pneuma.discovery import (
    ExpertDiscovery,
    DiscoveryConfig,
    DiscoveryPhase,
    SessionInit,
)
from lyceum.pneuma.messages import (
    RoutingRequest,
    ExpertOffer,
    Intent,
    Bid,
)


class TestExpertDiscovery:
    @pytest.fixture
    def discovery(self):
        return ExpertDiscovery()

    @pytest.fixture
    def sample_request(self):
        return RoutingRequest(
            id="req_001",
            origin="!node_moderator",
            intent=Intent(primary="code", secondary=["security"]),
        )

    @pytest.fixture
    def code_expert(self):
        return ExpertOffer(
            req_id="req_001",
            guardian_id="!node_coder",
            expert_type="qwen-2.5-coder-7b",
            capabilities=["code", "python"],
            bid=Bid(cost=0.1, est_latency_ms=500),
        )

    @pytest.fixture
    def security_expert(self):
        return ExpertOffer(
            req_id="req_001",
            guardian_id="!node_security",
            expert_type="qwen-2.5-security",
            capabilities=["security", "audit"],
            bid=Bid(cost=0.15, est_latency_ms=600),
        )

    def test_initial_phase_is_local(self, discovery):
        assert discovery.current_phase == DiscoveryPhase.LOCAL

    def test_escalate_to_backbone(self, discovery):
        discovery.escalate_to_backbone()
        assert discovery.current_phase == DiscoveryPhase.BACKBONE

    def test_add_and_select_single_offer(self, discovery, sample_request, code_expert):
        discovery.add_offer(code_expert)
        result = discovery.select_experts(sample_request)
        
        assert result.success is True
        assert result.proposer == code_expert
        assert result.critic is None

    def test_select_proposer_and_critic(
        self, discovery, sample_request, code_expert, security_expert
    ):
        discovery.add_offer(code_expert)
        discovery.add_offer(security_expert)
        result = discovery.select_experts(sample_request)
        
        assert result.success is True
        assert result.proposer == code_expert  # Matches primary intent
        assert result.critic == security_expert  # Matches secondary intent

    def test_no_offers_returns_failure(self, discovery, sample_request):
        result = discovery.select_experts(sample_request)
        assert result.success is False
        assert result.proposer is None

    def test_score_offer_with_reputation(self, discovery, code_expert):
        # Higher reputation should give higher score
        high_rep_score = discovery.score_offer(code_expert, reputation=90)
        low_rep_score = discovery.score_offer(code_expert, reputation=30)
        
        assert high_rep_score > low_rep_score

    def test_score_offer_with_latency(self, discovery):
        fast_expert = ExpertOffer(
            req_id="req",
            guardian_id="!fast",
            expert_type="model",
            capabilities=["code"],
            bid=Bid(cost=0.1, est_latency_ms=100),
        )
        slow_expert = ExpertOffer(
            req_id="req",
            guardian_id="!slow",
            expert_type="model",
            capabilities=["code"],
            bid=Bid(cost=0.1, est_latency_ms=2000),
        )
        
        # Same reputation, different latency
        fast_score = discovery.score_offer(fast_expert, reputation=50)
        slow_score = discovery.score_offer(slow_expert, reputation=50)
        
        assert fast_score > slow_score

    def test_reset_clears_state(self, discovery, code_expert):
        discovery.add_offer(code_expert)
        discovery.escalate_to_backbone()
        
        discovery.reset()
        
        assert discovery.current_phase == DiscoveryPhase.LOCAL
        assert len(discovery._offers) == 0

    def test_custom_config(self):
        config = DiscoveryConfig(
            local_timeout_ms=100,
            backbone_timeout_ms=5000,
            reputation_weight=0.7,
            latency_weight=0.3,
        )
        discovery = ExpertDiscovery(config=config)
        
        assert discovery.timeout_ms == 100
        discovery.escalate_to_backbone()
        assert discovery.timeout_ms == 5000


class TestSessionInit:
    def test_to_bytes(self):
        session = SessionInit(
            session_id="sess_12345678",
            request_id="req_001",
            proposer_id="!node_prop",
            critic_id="!node_crit",
            encrypted_prompt=b"encrypted_data_here",
        )
        
        data = session.to_bytes()
        
        # Header should be 32 + 16 + 16 + 16 = 80 bytes
        assert len(data) == 80 + len(b"encrypted_data_here")

    def test_to_bytes_no_critic(self):
        session = SessionInit(
            session_id="sess_001",
            request_id="req_001",
            proposer_id="!node_prop",
            critic_id=None,
            encrypted_prompt=b"data",
        )
        
        data = session.to_bytes()
        assert len(data) == 80 + 4
