"""
Sovereign AIWT Main Daemon

The main control loop for the self-contained AI Walkie-Talkie.
Coordinates the "Two Brains" architecture:
- Thinker (Radxa CPU): Runs AI models, sleeps when idle
- Listener (SX1262): Always-on LoRa radio, wakes Thinker on message

Control Flow:
1. Wait for input (PTT button or LoRa interrupt)
2. On PTT: Record → STT → Qwen Route → Transmit or Local Response
3. On LoRa RX: Decrypt → TTS → Play audio
"""
import asyncio
import logging
from dataclasses import dataclass
from typing import Optional, Callable
from enum import Enum

# Local imports (stubs for now)
from .stt import SenseVoiceSTT
from .tts import ParoliTTS
from .llm import QwenRouter
from .hardware import LoRaHAT, OLEDDisplay, ButtonEvent


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DaemonState(Enum):
    """AIWT daemon states."""
    IDLE = "idle"
    LISTENING = "listening"  # Recording user voice
    PROCESSING = "processing"  # Running AI pipeline
    TRANSMITTING = "transmitting"  # Sending over LoRa
    RECEIVING = "receiving"  # Incoming message
    SPEAKING = "speaking"  # Playing TTS output


@dataclass
class DaemonConfig:
    """Configuration for the AIWT daemon."""
    node_id: str = "!node_0001"
    channel: int = 4
    aes_key: Optional[bytes] = None
    # Hardware pins (Radxa Zero 3W GPIO)
    lora_irq_pin: int = 17
    ptt_pin: int = 27
    # Timeouts
    voice_timeout_ms: int = 5000
    pneuma_timeout_ms: int = 30000


class AIWTDaemon:
    """
    Main AIWT control daemon.
    
    Implements the "Digital Tripwire" workflow for message reception
    and the PTT workflow for transmission.
    """

    def __init__(self, config: Optional[DaemonConfig] = None):
        self.config = config or DaemonConfig()
        self.state = DaemonState.IDLE
        
        # Initialize components (lazy loading for actual hardware)
        self._stt: Optional[SenseVoiceSTT] = None
        self._tts: Optional[ParoliTTS] = None
        self._router: Optional[QwenRouter] = None
        self._lora: Optional[LoRaHAT] = None
        self._display: Optional[OLEDDisplay] = None
        
        # Callbacks
        self._on_message_received: Optional[Callable[[str], None]] = None
        self._on_message_sent: Optional[Callable[[str], None]] = None

    async def initialize(self):
        """Initialize all hardware and AI components."""
        logger.info("Initializing AIWT daemon...")
        
        # Initialize AI stack
        self._stt = SenseVoiceSTT()
        await self._stt.load_model()
        
        self._tts = ParoliTTS()
        await self._tts.load_model()
        
        self._router = QwenRouter()
        await self._router.load_model()
        
        # Initialize hardware
        self._lora = LoRaHAT(
            irq_pin=self.config.lora_irq_pin,
            channel=self.config.channel,
        )
        await self._lora.initialize()
        
        self._display = OLEDDisplay()
        await self._display.initialize()
        
        logger.info("AIWT daemon initialized")

    async def run(self):
        """
        Main event loop.
        
        Listens for:
        - PTT button press → Start voice recording
        - LoRa interrupt → Process incoming message
        - Pneuma button → Direct AI query
        """
        logger.info(f"AIWT daemon running as {self.config.node_id}")
        
        await self._display.show_status("Ready", self.config.node_id)
        
        # Create concurrent tasks for button and LoRa monitoring
        ptt_task = asyncio.create_task(self._monitor_ptt())
        lora_task = asyncio.create_task(self._monitor_lora())
        
        try:
            await asyncio.gather(ptt_task, lora_task)
        except asyncio.CancelledError:
            logger.info("Daemon shutdown requested")

    async def _monitor_ptt(self):
        """Monitor PTT button and handle voice recording."""
        while True:
            event = await self._wait_for_button(self.config.ptt_pin)
            
            if event == ButtonEvent.PRESSED:
                self.state = DaemonState.LISTENING
                await self._display.show_status("Recording...")
                
                # Record until button released
                audio = await self._record_until_released()
                
                # Process the voice input
                await self._process_voice_input(audio)

    async def _monitor_lora(self):
        """Monitor LoRa for incoming messages (Digital Tripwire)."""
        while True:
            # Wait for hardware interrupt from SX1262
            packet = await self._lora.receive()
            
            if packet:
                self.state = DaemonState.RECEIVING
                await self._display.show_status("Message received")
                
                # Decrypt and process
                await self._process_incoming_message(packet)

    async def _process_voice_input(self, audio: bytes):
        """
        Process recorded voice through the AI pipeline.
        
        Pipeline: Audio → STT → Router → (Transmit or TTS)
        """
        self.state = DaemonState.PROCESSING
        await self._display.show_status("Processing...")
        
        # Speech-to-Text
        text = await self._stt.transcribe(audio)
        logger.info(f"Transcribed: {text}")
        
        # Route through Qwen
        response = await self._router.route(text)
        
        if response.should_transmit:
            # Send over LoRa
            self.state = DaemonState.TRANSMITTING
            await self._lora.send(response.text, self.config.channel)
            await self._display.show_status("Sent!")
            
            if self._on_message_sent:
                self._on_message_sent(response.text)
        else:
            # Local response - play via TTS
            self.state = DaemonState.SPEAKING
            audio_out = await self._tts.synthesize(response.text)
            await self._play_audio(audio_out)
        
        self.state = DaemonState.IDLE
        await self._display.show_status("Ready")

    async def _process_incoming_message(self, packet: bytes):
        """Process an incoming LoRa message."""
        # Decrypt packet
        plaintext = self._decrypt(packet)
        if not plaintext:
            logger.warning("Failed to decrypt incoming packet")
            return
        
        text = plaintext.decode("utf-8")
        logger.info(f"Received: {text}")
        
        # Convert to speech
        self.state = DaemonState.SPEAKING
        await self._display.show_message(text)
        
        audio = await self._tts.synthesize(text)
        await self._play_audio(audio)
        
        if self._on_message_received:
            self._on_message_received(text)
        
        self.state = DaemonState.IDLE
        await self._display.show_status("Ready")

    def _decrypt(self, packet: bytes) -> Optional[bytes]:
        """Decrypt an incoming packet using AES-GCM."""
        if not self.config.aes_key:
            return packet  # No encryption configured
        
        # Use lyceum crypto module
        from lyceum.crypto import AESGCMCipher
        cipher = AESGCMCipher(self.config.aes_key)
        return cipher.decrypt(packet)

    # Placeholder methods for hardware interaction
    async def _wait_for_button(self, pin: int) -> ButtonEvent:
        """Wait for button event on GPIO pin."""
        await asyncio.sleep(0.1)  # Stub
        return ButtonEvent.RELEASED

    async def _record_until_released(self) -> bytes:
        """Record audio until PTT released."""
        return b""  # Stub

    async def _play_audio(self, audio: bytes):
        """Play audio through speaker."""
        pass  # Stub


async def main():
    """Entry point for running the daemon."""
    daemon = AIWTDaemon()
    await daemon.initialize()
    await daemon.run()


if __name__ == "__main__":
    asyncio.run(main())
