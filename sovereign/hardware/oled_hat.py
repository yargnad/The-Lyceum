"""
Waveshare 1.3" OLED HAT Driver

Driver for the Waveshare 1.3inch OLED HAT with 5-way joystick and 3 buttons.
Display: 128x64 SH1106 OLED

HAT: Waveshare 1.3inch OLED HAT
"""
import asyncio
import logging
from dataclasses import dataclass
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class OLEDConfig:
    """Configuration for the OLED display."""
    width: int = 128
    height: int = 64
    i2c_bus: int = 1
    i2c_address: int = 0x3C
    # Font settings
    font_size: int = 12
    line_height: int = 14


class OLEDDisplay:
    """
    Waveshare OLED HAT display driver.
    
    This is a stub implementation. Production version will use:
    - luma.oled for display rendering
    - PIL for text/image composition
    """

    def __init__(self, config: Optional[OLEDConfig] = None):
        self.config = config or OLEDConfig()
        self._display = None
        self._initialized = False

    async def initialize(self):
        """
        Initialize the OLED display.
        
        Production implementation:
        ```python
        from luma.core.interface.serial import i2c
        from luma.oled.device import sh1106
        
        serial = i2c(port=self.config.i2c_bus, address=self.config.i2c_address)
        self._display = sh1106(serial)
        ```
        """
        logger.info("Initializing OLED display...")
        
        self._initialized = True
        logger.info("OLED display initialized (stub)")

    async def clear(self):
        """Clear the display."""
        if not self._initialized:
            return
        logger.debug("Display cleared")

    async def show_status(self, status: str, node_id: str = ""):
        """
        Show status message on display.
        
        Layout:
        +------------------+
        | [Node ID]        |
        |                  |
        |   [STATUS]       |
        |                  |
        +------------------+
        """
        if not self._initialized:
            return
        
        logger.info(f"Display: {status}")

    async def show_message(self, message: str, sender: str = ""):
        """
        Show incoming message on display.
        
        Layout:
        +------------------+
        | From: [sender]   |
        +------------------+
        | [message text    |
        |  wrapped across  |
        |  multiple lines] |
        +------------------+
        """
        if not self._initialized:
            return
        
        logger.info(f"Display message from {sender}: {message[:30]}...")

    async def show_menu(self, items: list, selected: int = 0):
        """Show a menu with selectable items."""
        if not self._initialized:
            return
        
        for i, item in enumerate(items):
            prefix = ">" if i == selected else " "
            logger.debug(f"{prefix} {item}")

    async def show_signal_strength(self, rssi: int, snr: float):
        """Show signal strength indicator."""
        bars = max(0, min(4, (rssi + 120) // 10))
        logger.debug(f"Signal: {'█' * bars}{'░' * (4-bars)} {rssi}dBm")

    def close(self):
        """Release display resources."""
        self._initialized = False
        logger.info("OLED display closed")
