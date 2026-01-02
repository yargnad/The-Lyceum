"""
Pneuma Intent Router (Stage A - CLASSIFY)

Implements the local intent classification step from PNEUMA_PROTOCOL.md:
- User provides input
- Local classifier determines intent and sensitivity
- Output feeds into discovery phase

In production, this would use a quantized model (TinyBERT/Qwen-3B).
This stub provides a rule-based fallback for testing.
"""
from dataclasses import dataclass
from typing import List, Tuple, Optional
from enum import Enum
import re

from .messages import Intent, IntentConstraints, RoutingRequest


class IntentType(Enum):
    """Primary intent categories for the Gating Network."""
    CODE = "code"
    SECURITY = "security"
    GENERAL = "general"
    MATH = "math"
    CREATIVE = "creative"
    UNKNOWN = "unknown"


class Sensitivity(Enum):
    """Sensitivity level for routing decisions."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass
class ClassificationResult:
    """Output from the intent classifier."""
    intent_type: IntentType
    confidence: float
    sensitivity: Sensitivity
    secondary_intents: List[IntentType]

    def to_intent(self) -> Intent:
        """Convert to protocol Intent message."""
        return Intent(
            primary=self.intent_type.value,
            secondary=[s.value for s in self.secondary_intents],
            confidence=self.confidence,
        )


class IntentClassifier:
    """
    Rule-based intent classifier (stub for LLM-based classifier).
    
    In production, this would wrap a quantized Qwen 2.5 3B model
    running on the Rockchip NPU. This provides a lightweight fallback.
    """

    # Keyword patterns for rule-based classification
    CODE_PATTERNS = [
        r"\b(code|script|function|program|python|javascript|rust|golang|c\+\+)\b",
        r"\b(implement|debug|fix|refactor|write|create)\b.*\b(code|function|class)\b",
        r"\bdef\s+\w+|class\s+\w+|function\s+\w+",
    ]

    SECURITY_PATTERNS = [
        r"\b(security|vulnerability|exploit|attack|encrypt|decrypt|auth)\b",
        r"\b(password|credential|token|key|certificate|ssl|tls)\b",
        r"\b(injection|xss|csrf|sqli|rce)\b",
    ]

    MATH_PATTERNS = [
        r"\b(calculate|compute|solve|equation|formula|integral|derivative)\b",
        r"\b(math|algebra|calculus|statistics|probability)\b",
        r"[\d\+\-\*\/\=\(\)]{5,}",  # Expressions with operators
    ]

    CREATIVE_PATTERNS = [
        r"\b(write|compose|create|generate)\b.*\b(story|poem|song|essay)\b",
        r"\b(creative|artistic|imaginative|fiction)\b",
    ]

    def __init__(self):
        self._compile_patterns()

    def _compile_patterns(self):
        """Pre-compile regex patterns for efficiency."""
        self._code_re = [re.compile(p, re.IGNORECASE) for p in self.CODE_PATTERNS]
        self._security_re = [re.compile(p, re.IGNORECASE) for p in self.SECURITY_PATTERNS]
        self._math_re = [re.compile(p, re.IGNORECASE) for p in self.MATH_PATTERNS]
        self._creative_re = [re.compile(p, re.IGNORECASE) for p in self.CREATIVE_PATTERNS]

    def _match_score(self, text: str, patterns: List[re.Pattern]) -> float:
        """Count pattern matches normalized to [0, 1]."""
        matches = sum(1 for p in patterns if p.search(text))
        return min(matches / max(len(patterns), 1), 1.0)

    def classify(self, text: str) -> ClassificationResult:
        """
        Classify user input into intent categories.
        
        Args:
            text: User's natural language input
            
        Returns:
            ClassificationResult with intent, confidence, and sensitivity
        """
        scores = {
            IntentType.CODE: self._match_score(text, self._code_re),
            IntentType.SECURITY: self._match_score(text, self._security_re),
            IntentType.MATH: self._match_score(text, self._math_re),
            IntentType.CREATIVE: self._match_score(text, self._creative_re),
        }

        # Find primary intent (highest score)
        sorted_intents = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        primary, primary_score = sorted_intents[0]

        # Fall back to GENERAL if no strong match
        if primary_score < 0.2:
            primary = IntentType.GENERAL
            primary_score = 0.5

        # Collect secondary intents (score > 0.3)
        secondary = [
            intent for intent, score in sorted_intents[1:]
            if score > 0.3
        ]

        # Determine sensitivity
        sensitivity = Sensitivity.LOW
        if IntentType.SECURITY in [primary] + secondary:
            sensitivity = Sensitivity.HIGH
        elif IntentType.CODE in [primary] + secondary:
            sensitivity = Sensitivity.MEDIUM

        return ClassificationResult(
            intent_type=primary,
            confidence=min(primary_score + 0.5, 1.0),  # Boost base confidence
            sensitivity=sensitivity,
            secondary_intents=secondary,
        )

    def create_routing_request(
        self,
        text: str,
        node_id: str,
        request_id: str,
        constraints: Optional[IntentConstraints] = None,
    ) -> RoutingRequest:
        """
        Classify input and create a RoutingRequest message.
        
        Args:
            text: User's natural language input
            node_id: This node's ID (e.g., "!node_a1b2")
            request_id: Unique request identifier
            constraints: Optional user-specified constraints
            
        Returns:
            RoutingRequest ready for broadcast
        """
        result = self.classify(text)
        return RoutingRequest(
            id=request_id,
            origin=node_id,
            intent=result.to_intent(),
            constraints=constraints or IntentConstraints(),
            payload_hash=RoutingRequest.hash_payload(text),
        )
