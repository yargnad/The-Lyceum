"""Tests for intent classification router."""
import pytest
from lyceum.pneuma.router import (
    IntentClassifier,
    IntentType,
    Sensitivity,
    ClassificationResult,
)
from lyceum.pneuma.messages import IntentConstraints


class TestIntentClassifier:
    @pytest.fixture
    def classifier(self):
        return IntentClassifier()

    def test_classify_code_intent(self, classifier):
        result = classifier.classify("Write a Python function to sort a list")
        assert result.intent_type == IntentType.CODE
        assert result.confidence > 0.5

    def test_classify_security_intent(self, classifier):
        result = classifier.classify("Check for SQL injection vulnerabilities")
        assert result.intent_type == IntentType.SECURITY
        assert result.sensitivity == Sensitivity.HIGH

    def test_classify_math_intent(self, classifier):
        result = classifier.classify("Calculate the integral of x^2")
        assert result.intent_type == IntentType.MATH

    def test_classify_creative_intent(self, classifier):
        result = classifier.classify("Write a creative story about space exploration")
        assert result.intent_type == IntentType.CREATIVE

    def test_classify_general_fallback(self, classifier):
        result = classifier.classify("Hello, how are you today?")
        assert result.intent_type == IntentType.GENERAL

    def test_secondary_intents(self, classifier):
        result = classifier.classify(
            "Write a secure Python script that encrypts passwords"
        )
        # Should detect both code and security
        all_intents = [result.intent_type] + result.secondary_intents
        assert IntentType.CODE in all_intents or IntentType.SECURITY in all_intents

    def test_to_intent_conversion(self, classifier):
        result = classifier.classify("Debug this JavaScript code")
        intent = result.to_intent()
        assert intent.primary == result.intent_type.value
        assert len(intent.secondary) == len(result.secondary_intents)


class TestCreateRoutingRequest:
    @pytest.fixture
    def classifier(self):
        return IntentClassifier()

    def test_create_routing_request(self, classifier):
        req = classifier.create_routing_request(
            text="Write a Python script",
            node_id="!node_test",
            request_id="req_001",
        )
        
        assert req.id == "req_001"
        assert req.origin == "!node_test"
        assert req.intent.primary == "code"
        assert req.payload_hash != ""

    def test_create_with_constraints(self, classifier):
        constraints = IntentConstraints(max_latency_ms=500, prefer_local=True)
        req = classifier.create_routing_request(
            text="Quick math calculation",
            node_id="!node_test",
            request_id="req_002",
            constraints=constraints,
        )
        
        assert req.constraints.max_latency_ms == 500
        assert req.constraints.prefer_local is True

    def test_payload_hash_deterministic(self, classifier):
        req1 = classifier.create_routing_request("test", "!n", "r1")
        req2 = classifier.create_routing_request("test", "!n", "r2")
        
        assert req1.payload_hash == req2.payload_hash
