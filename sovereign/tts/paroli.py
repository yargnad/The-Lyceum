"""
Paroli Text-to-Speech Wrapper

NPU-accelerated speech synthesis optimized for Rockchip hardware.
Generates speech 5x faster than real-time with a tiny 35MB footprint.

Library: https://github.com/marty1885/paroli
"""
import logging
from dataclasses import dataclass
from typing import Optional
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass
class TTSConfig:
    """Configuration for Paroli TTS."""
    model_path: str = "/opt/lyceum/models/paroli"
    sample_rate: int = 22050
    voice: str = "default"
    speed: float = 1.0
    # Audio output
    output_format: str = "pcm"  # pcm, wav, mp3


class ParoliTTS:
    """
    Paroli NPU-accelerated text-to-speech.
    
    This is a stub implementation. Production version will use:
    - paroli Python bindings
    - RKNN NPU acceleration
    - Audio output via ALSA
    """

    def __init__(self, config: Optional[TTSConfig] = None):
        self.config = config or TTSConfig()
        self._engine = None
        self._loaded = False

    async def load_model(self):
        """
        Load the Paroli TTS model.
        
        Production implementation:
        ```python
        import paroli
        self._engine = paroli.TTS(
            model_path=self.config.model_path,
            device="npu"
        )
        ```
        """
        logger.info(f"Loading Paroli TTS from {self.config.model_path}")
        
        # Check if model directory exists
        model_path = Path(self.config.model_path)
        if not model_path.exists():
            logger.warning(f"Model not found at {model_path}, using stub mode")
        
        self._loaded = True
        logger.info("Paroli TTS loaded (stub)")

    async def synthesize(self, text: str) -> bytes:
        """
        Convert text to speech audio.
        
        Args:
            text: Text to synthesize
            
        Returns:
            Raw PCM audio data (22.05kHz, 16-bit, mono)
        """
        if not self._loaded:
            raise RuntimeError("Model not loaded. Call load_model() first.")
        
        logger.info(f"Synthesizing: '{text[:50]}...' ({len(text)} chars)")
        
        # Production would:
        # 1. Normalize text (expand abbreviations, numbers)
        # 2. Run phoneme conversion
        # 3. Generate mel spectrogram via NPU
        # 4. Vocode to audio waveform
        
        # Stub: return empty audio
        return b""

    async def synthesize_to_file(self, text: str, output_path: str):
        """Synthesize speech and save to file."""
        audio = await self.synthesize(text)
        
        # In production, add proper WAV header
        with open(output_path, "wb") as f:
            f.write(audio)
        
        logger.info(f"Saved audio to {output_path}")

    def set_voice(self, voice: str):
        """Change the TTS voice."""
        self.config.voice = voice
        logger.info(f"Voice set to: {voice}")

    def set_speed(self, speed: float):
        """Adjust speech speed (0.5 = half speed, 2.0 = double)."""
        self.config.speed = max(0.25, min(4.0, speed))
        logger.info(f"Speed set to: {self.config.speed}")

    def unload_model(self):
        """Release resources."""
        if self._engine:
            self._engine = None
        self._loaded = False
        logger.info("Paroli TTS unloaded")
