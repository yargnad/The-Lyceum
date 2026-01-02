"""
Pneuma Expert Discovery (Stage B - Two-Phase Routing)

Implements the discovery protocol from PNEUMA_PROTOCOL.md:
- Phase 1 (Local): Query Layer 2 (Wi-Fi HaLow) mesh for nearby Guardians
- Phase 2 (Backbone): Escalate to Layer 3 (LoRa PTP) if no local expert found

Selection uses weighted scoring: (Reputation * 0.6) + (1/Latency * 0.4)
"""
from dataclasses import dataclass, field
from typing import List, Optional, Callable, Awaitable
from enum import Enum
import time

from .messages import RoutingRequest, ExpertOffer, Bid


class DiscoveryPhase(Enum):
    """Current phase of expert discovery."""
    LOCAL = "local"      # Layer 2 discovery
    BACKBONE = "backbone"  # Layer 3 escalation


@dataclass
class DiscoveryConfig:
    """Configuration for discovery timeouts and scoring."""
    # Timeout for local Layer 2 discovery (ms)
    local_timeout_ms: int = 200
    # Timeout for backbone Layer 3 discovery (ms)
    backbone_timeout_ms: int = 2000
    # Scoring weights
    reputation_weight: float = 0.6
    latency_weight: float = 0.4
    # Minimum offers to consider before selecting
    min_offers: int = 1


@dataclass
class DiscoveryResult:
    """Result of the expert discovery process."""
    phase: DiscoveryPhase
    proposer: Optional[ExpertOffer] = None
    critic: Optional[ExpertOffer] = None
    all_offers: List[ExpertOffer] = field(default_factory=list)
    latency_ms: int = 0

    @property
    def success(self) -> bool:
        return self.proposer is not None


class ExpertDiscovery:
    """
    Two-phase expert discovery protocol.
    
    The Moderator first queries the local Layer 2 mesh, then escalates
    to the Layer 3 backbone if no suitable expert is found.
    """

    def __init__(self, config: Optional[DiscoveryConfig] = None):
        self.config = config or DiscoveryConfig()
        self._offers: List[ExpertOffer] = []
        self._phase = DiscoveryPhase.LOCAL

    def reset(self):
        """Reset discovery state for a new request."""
        self._offers = []
        self._phase = DiscoveryPhase.LOCAL

    def add_offer(self, offer: ExpertOffer):
        """Register an incoming ExpertOffer."""
        self._offers.append(offer)

    def score_offer(self, offer: ExpertOffer, reputation: int = 50) -> float:
        """
        Score an offer using the protocol formula:
        score = (Reputation * 0.6) + (1/Latency * 0.4)
        
        Args:
            offer: The ExpertOffer to score
            reputation: Node's reputation from Pneuma Vault (default 50)
            
        Returns:
            Weighted score (higher is better)
        """
        # Normalize reputation to [0, 1] assuming max of 100
        rep_normalized = min(reputation / 100.0, 1.0)
        
        # Normalize latency (lower is better, cap at 5000ms)
        lat_normalized = 1.0 / max(offer.bid.est_latency_ms, 1)
        lat_normalized = min(lat_normalized * 1000, 1.0)  # Scale for reasonable range
        
        return (
            rep_normalized * self.config.reputation_weight +
            lat_normalized * self.config.latency_weight
        )

    def select_experts(
        self,
        request: RoutingRequest,
        reputation_lookup: Optional[Callable[[str], int]] = None,
    ) -> DiscoveryResult:
        """
        Select the best proposer and critic from collected offers.
        
        Args:
            request: The original RoutingRequest
            reputation_lookup: Optional function to get node reputation
            
        Returns:
            DiscoveryResult with selected experts
        """
        if not self._offers:
            return DiscoveryResult(
                phase=self._phase,
                all_offers=[],
            )

        # Default reputation lookup returns base value
        get_rep = reputation_lookup or (lambda _: 50)

        # Score all offers
        scored = [
            (offer, self.score_offer(offer, get_rep(offer.guardian_id)))
            for offer in self._offers
        ]
        scored.sort(key=lambda x: x[1], reverse=True)

        # Select best proposer (matches primary intent)
        proposer = None
        for offer, score in scored:
            if request.intent.primary in offer.capabilities:
                proposer = offer
                break

        # Select best critic (matches secondary intent, different from proposer)
        critic = None
        if request.intent.secondary:
            for offer, score in scored:
                if offer != proposer:
                    for skill in request.intent.secondary:
                        if skill in offer.capabilities:
                            critic = offer
                            break
                    if critic:
                        break

        return DiscoveryResult(
            phase=self._phase,
            proposer=proposer,
            critic=critic,
            all_offers=self._offers.copy(),
        )

    def escalate_to_backbone(self):
        """Escalate discovery to Layer 3 backbone."""
        self._phase = DiscoveryPhase.BACKBONE

    @property
    def current_phase(self) -> DiscoveryPhase:
        return self._phase

    @property
    def timeout_ms(self) -> int:
        """Get timeout for current phase."""
        if self._phase == DiscoveryPhase.LOCAL:
            return self.config.local_timeout_ms
        return self.config.backbone_timeout_ms


@dataclass
class SessionInit:
    """
    Session initialization message sent after expert selection.
    Contains the full prompt, encrypted with selected Guardians' public keys.
    """
    session_id: str
    request_id: str
    proposer_id: str
    critic_id: Optional[str]
    encrypted_prompt: bytes  # ECDH-encrypted payload

    def to_bytes(self) -> bytes:
        """Serialize for transmission."""
        header = (
            self.session_id.encode("utf-8")[:32].ljust(32, b"\x00") +
            self.request_id.encode("utf-8")[:16].ljust(16, b"\x00") +
            self.proposer_id.encode("utf-8")[:16].ljust(16, b"\x00") +
            (self.critic_id or "").encode("utf-8")[:16].ljust(16, b"\x00")
        )
        return header + self.encrypted_prompt
