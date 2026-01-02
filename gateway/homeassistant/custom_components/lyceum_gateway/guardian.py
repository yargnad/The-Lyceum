"""
Lyceum Guardian Daemon for Home Assistant

Enables HA servers to contribute compute resources to the Pneuma network.
Users can opt-in to:
- Reflex jobs (STT/TTS for other nodes)
- Cortex jobs (federated LLM inference)
- Symbolon hosting (containerized apps)
- Backbone relay (internet bridging)

All contributions earn Proof-of-Utility tokens.
"""
from __future__ import annotations

import asyncio
import logging
import psutil
from dataclasses import dataclass, field
from typing import Any, Callable, Optional
from datetime import datetime
from enum import Enum, auto

from homeassistant.core import HomeAssistant

_LOGGER = logging.getLogger(__name__)


class GuardianSkill(Enum):
    """Skills a Guardian can offer to the network."""
    RELAY = "relay"           # Backbone relay
    REFLEX_STT = "reflex_stt"  # Speech-to-text
    REFLEX_TTS = "reflex_tts"  # Text-to-speech
    CORTEX = "cortex"          # LLM inference
    SYMBOLON = "symbolon"      # App hosting


@dataclass
class ResourceLimits:
    """Resource limits for Guardian compute contributions."""
    cpu_percent: int = 25      # Max CPU usage
    memory_mb: int = 512       # Max memory
    jobs_per_hour: int = 100   # Rate limit
    max_concurrent: int = 2    # Max parallel jobs


@dataclass
class GuardianConfig:
    """Configuration for Guardian mode."""
    enabled: bool = False
    node_id: str = "!ha_guardian"
    skills: list[str] = field(default_factory=lambda: ["relay"])
    limits: ResourceLimits = field(default_factory=ResourceLimits)
    symbolons: list[str] = field(default_factory=list)
    earn_tokens: bool = True   # Participate in Proof-of-Utility


@dataclass
class JobResult:
    """Result of a completed job."""
    job_id: str
    success: bool
    result: Any
    duration_ms: int
    tokens_earned: float = 0.0


class GuardianDaemon:
    """
    Guardian daemon running on Home Assistant.
    
    Listens for Pneuma job requests and executes them
    within configured resource limits.
    """

    def __init__(self, hass: HomeAssistant, config: GuardianConfig):
        self.hass = hass
        self.config = config
        self._running = False
        self._active_jobs: dict[str, asyncio.Task] = {}
        self._job_count = 0
        self._tokens_earned = 0.0
        
        # Skill handlers
        self._handlers: dict[GuardianSkill, Callable] = {}
        
        # Symbolon runtime
        self._symbolon_runtime: Optional[SymbolonRuntime] = None

    async def async_start(self) -> None:
        """Start the Guardian daemon."""
        if not self.config.enabled:
            _LOGGER.info("Guardian mode disabled")
            return
        
        _LOGGER.info(
            "Starting Guardian daemon: %s with skills %s",
            self.config.node_id,
            self.config.skills,
        )
        
        # Register skill handlers
        self._register_handlers()
        
        # Initialize Symbolon runtime if enabled
        if GuardianSkill.SYMBOLON.value in self.config.skills:
            self._symbolon_runtime = SymbolonRuntime(
                self.hass,
                allowed_symbolons=self.config.symbolons,
            )
            await self._symbolon_runtime.async_start()
        
        self._running = True
        
        # Register with the network
        await self._announce_availability()

    async def async_stop(self) -> None:
        """Stop the Guardian daemon."""
        self._running = False
        
        # Cancel active jobs
        for job_id, task in self._active_jobs.items():
            task.cancel()
            _LOGGER.info("Cancelled job: %s", job_id)
        
        # Stop Symbolon runtime
        if self._symbolon_runtime:
            await self._symbolon_runtime.async_stop()
        
        _LOGGER.info("Guardian daemon stopped. Tokens earned: %.2f", self._tokens_earned)

    def _register_handlers(self) -> None:
        """Register handlers for enabled skills."""
        if GuardianSkill.RELAY.value in self.config.skills:
            self._handlers[GuardianSkill.RELAY] = self._handle_relay
        
        if GuardianSkill.REFLEX_STT.value in self.config.skills:
            self._handlers[GuardianSkill.REFLEX_STT] = self._handle_stt
        
        if GuardianSkill.REFLEX_TTS.value in self.config.skills:
            self._handlers[GuardianSkill.REFLEX_TTS] = self._handle_tts
        
        if GuardianSkill.CORTEX.value in self.config.skills:
            self._handlers[GuardianSkill.CORTEX] = self._handle_cortex

    async def _announce_availability(self) -> None:
        """Announce this Guardian's availability to the network."""
        # This would send an ExpertOffer via the gateway
        announcement = {
            "type": "guardian_announce",
            "node_id": self.config.node_id,
            "skills": self.config.skills,
            "limits": {
                "cpu": self.config.limits.cpu_percent,
                "memory": self.config.limits.memory_mb,
                "rate": self.config.limits.jobs_per_hour,
            },
            "symbolons": self.config.symbolons,
        }
        _LOGGER.info("Guardian announced: %s", announcement)

    async def handle_job_request(self, job: dict) -> JobResult:
        """
        Handle an incoming job request.
        
        Validates resource availability, executes the job,
        and returns the result.
        """
        job_id = job.get("id", f"job_{self._job_count}")
        skill = job.get("skill")
        
        # Check if we handle this skill
        skill_enum = GuardianSkill(skill) if skill else None
        if skill_enum not in self._handlers:
            return JobResult(
                job_id=job_id,
                success=False,
                result={"error": f"Skill not supported: {skill}"},
                duration_ms=0,
            )
        
        # Check resource limits
        if not self._check_resources():
            return JobResult(
                job_id=job_id,
                success=False,
                result={"error": "Resource limits exceeded"},
                duration_ms=0,
            )
        
        # Check concurrency limit
        if len(self._active_jobs) >= self.config.limits.max_concurrent:
            return JobResult(
                job_id=job_id,
                success=False,
                result={"error": "Max concurrent jobs reached"},
                duration_ms=0,
            )
        
        # Execute the job
        start_time = datetime.now()
        try:
            handler = self._handlers[skill_enum]
            result = await handler(job)
            success = True
        except Exception as e:
            _LOGGER.error("Job %s failed: %s", job_id, e)
            result = {"error": str(e)}
            success = False
        
        duration_ms = int((datetime.now() - start_time).total_seconds() * 1000)
        
        # Calculate tokens earned
        tokens = self._calculate_tokens(skill_enum, duration_ms, success)
        if self.config.earn_tokens:
            self._tokens_earned += tokens
        
        self._job_count += 1
        
        return JobResult(
            job_id=job_id,
            success=success,
            result=result,
            duration_ms=duration_ms,
            tokens_earned=tokens,
        )

    def _check_resources(self) -> bool:
        """Check if current resource usage allows more jobs."""
        cpu = psutil.cpu_percent()
        mem = psutil.virtual_memory()
        mem_used_mb = (mem.total - mem.available) / (1024 * 1024)
        
        if cpu > self.config.limits.cpu_percent * 2:  # Allow some headroom
            _LOGGER.warning("CPU too high: %.1f%%", cpu)
            return False
        
        # Check memory headroom
        if mem.percent > 90:
            _LOGGER.warning("Memory too high: %.1f%%", mem.percent)
            return False
        
        return True

    def _calculate_tokens(
        self,
        skill: GuardianSkill,
        duration_ms: int,
        success: bool,
    ) -> float:
        """Calculate tokens earned for a job."""
        if not success:
            return 0.0
        
        # Base rates from PROOF_OF_UTILITY.md
        base_rates = {
            GuardianSkill.RELAY: 0.02,
            GuardianSkill.REFLEX_STT: 0.05,
            GuardianSkill.REFLEX_TTS: 0.03,
            GuardianSkill.CORTEX: 0.10,
            GuardianSkill.SYMBOLON: 0.05,
        }
        
        return base_rates.get(skill, 0.01)

    # Skill handlers
    async def _handle_relay(self, job: dict) -> dict:
        """Handle backbone relay job."""
        message = job.get("message", "")
        destination = job.get("destination")
        
        # Would forward via internet or re-transmit on mesh
        _LOGGER.info("Relay job: %s -> %s", message[:30], destination)
        
        return {"relayed": True, "destination": destination}

    async def _handle_stt(self, job: dict) -> dict:
        """Handle speech-to-text job."""
        audio_data = job.get("audio")
        
        # Stub - would use actual STT model
        _LOGGER.info("STT job: %d bytes audio", len(audio_data) if audio_data else 0)
        
        return {"text": "[STT placeholder - model not loaded]"}

    async def _handle_tts(self, job: dict) -> dict:
        """Handle text-to-speech job."""
        text = job.get("text", "")
        
        # Stub - would use actual TTS model
        _LOGGER.info("TTS job: %s", text[:50])
        
        return {"audio": b"", "format": "pcm"}

    async def _handle_cortex(self, job: dict) -> dict:
        """Handle LLM inference job."""
        prompt = job.get("prompt", "")
        
        # Stub - would use actual LLM
        _LOGGER.info("Cortex job: %s", prompt[:50])
        
        return {"response": "[LLM placeholder - model not loaded]"}

    @property
    def stats(self) -> dict:
        """Get Guardian statistics."""
        return {
            "running": self._running,
            "node_id": self.config.node_id,
            "skills": self.config.skills,
            "jobs_completed": self._job_count,
            "active_jobs": len(self._active_jobs),
            "tokens_earned": self._tokens_earned,
        }


class SymbolonRuntime:
    """
    Runtime for executing Symbolon applications.
    
    Symbolons run in isolated containers with resource limits.
    """

    def __init__(
        self,
        hass: HomeAssistant,
        allowed_symbolons: list[str],
    ):
        self.hass = hass
        self.allowed = set(allowed_symbolons)
        self._running_apps: dict[str, Any] = {}

    async def async_start(self) -> None:
        """Start the Symbolon runtime."""
        _LOGGER.info("Symbolon runtime started. Allowed: %s", self.allowed)

    async def async_stop(self) -> None:
        """Stop all running Symbolons."""
        for name in list(self._running_apps.keys()):
            await self.stop_symbolon(name)
        _LOGGER.info("Symbolon runtime stopped")

    async def start_symbolon(self, name: str) -> bool:
        """Start a Symbolon application."""
        if name not in self.allowed:
            _LOGGER.warning("Symbolon not allowed: %s", name)
            return False
        
        if name in self._running_apps:
            _LOGGER.info("Symbolon already running: %s", name)
            return True
        
        # Would pull container image and start it
        _LOGGER.info("Starting Symbolon: %s", name)
        self._running_apps[name] = {"started": datetime.now()}
        
        return True

    async def stop_symbolon(self, name: str) -> bool:
        """Stop a Symbolon application."""
        if name not in self._running_apps:
            return False
        
        # Would stop the container
        _LOGGER.info("Stopping Symbolon: %s", name)
        del self._running_apps[name]
        
        return True

    async def invoke_symbolon(self, name: str, request: dict) -> dict:
        """Invoke a running Symbolon."""
        if name not in self._running_apps:
            return {"error": f"Symbolon not running: {name}"}
        
        # Would call the container's API
        _LOGGER.info("Invoking Symbolon %s: %s", name, request)
        
        return {"result": "[Symbolon response placeholder]"}

    @property
    def running(self) -> list[str]:
        """Get list of running Symbolons."""
        return list(self._running_apps.keys())
