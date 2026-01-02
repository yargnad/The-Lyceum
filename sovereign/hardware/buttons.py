"""
Button and Joystick Handler

Handles the 8-button control scheme from the Waveshare OLED HAT:
- 5-way joystick (up, down, left, right, center/press)
- 3 side buttons (power/menu, inbox/replay, pneuma)

GPIO assignments for Radxa Zero 3W / Raspberry Pi compatible.
"""
import asyncio
import logging
from enum import Enum, auto
from dataclasses import dataclass
from typing import Optional, Callable

logger = logging.getLogger(__name__)


class ButtonEvent(Enum):
    """Button event types."""
    PRESSED = auto()
    RELEASED = auto()
    LONG_PRESS = auto()  # Held > 1 second


class Button(Enum):
    """Physical buttons on the device."""
    # Joystick directions
    JOY_UP = auto()
    JOY_DOWN = auto()
    JOY_LEFT = auto()
    JOY_RIGHT = auto()
    JOY_CENTER = auto()  # PTT (Push-to-Talk)
    # Side buttons
    BTN_POWER = auto()    # Power / Main Menu
    BTN_INBOX = auto()    # Inbox / Replay
    BTN_PNEUMA = auto()   # Pneuma AI Query


@dataclass
class ButtonConfig:
    """GPIO pin assignments for buttons."""
    # Joystick pins (active low)
    joy_up: int = 5
    joy_down: int = 6
    joy_left: int = 13
    joy_right: int = 19
    joy_center: int = 26
    # Side button pins
    btn_power: int = 16
    btn_inbox: int = 20
    btn_pneuma: int = 21
    # Timing
    debounce_ms: int = 50
    long_press_ms: int = 1000


class ButtonHandler:
    """
    Button and joystick input handler.
    
    This is a stub implementation. Production version will use:
    - RPi.GPIO or gpiod for GPIO input
    - Hardware interrupts for low-latency response
    """

    def __init__(self, config: Optional[ButtonConfig] = None):
        self.config = config or ButtonConfig()
        self._callbacks: dict[Button, list[Callable]] = {}
        self._initialized = False

    async def initialize(self):
        """
        Initialize GPIO inputs for all buttons.
        
        Production implementation:
        ```python
        import RPi.GPIO as GPIO
        GPIO.setmode(GPIO.BCM)
        for pin in [self.config.joy_up, ...]:
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.add_event_detect(pin, GPIO.BOTH, callback=self._handle_gpio)
        ```
        """
        logger.info("Initializing button handler...")
        
        self._initialized = True
        logger.info("Button handler initialized (stub)")

    def on_button(self, button: Button, callback: Callable[[ButtonEvent], None]):
        """Register a callback for button events."""
        if button not in self._callbacks:
            self._callbacks[button] = []
        self._callbacks[button].append(callback)

    async def wait_for_button(self, button: Button, timeout_ms: int = 0) -> Optional[ButtonEvent]:
        """
        Wait for a specific button event.
        
        Args:
            button: Which button to wait for
            timeout_ms: Maximum wait time (0 = infinite)
            
        Returns:
            ButtonEvent on success, None on timeout
        """
        if not self._initialized:
            raise RuntimeError("Handler not initialized")
        
        logger.debug(f"Waiting for {button.name}...")
        
        # Stub: simulate button press after short delay
        try:
            await asyncio.wait_for(
                asyncio.sleep(timeout_ms / 1000 if timeout_ms else 3600),
                timeout=timeout_ms / 1000 if timeout_ms else None,
            )
        except asyncio.TimeoutError:
            return None
        
        return ButtonEvent.RELEASED

    async def wait_for_any(self, timeout_ms: int = 0) -> Optional[tuple[Button, ButtonEvent]]:
        """Wait for any button event."""
        # Stub: return None (timeout)
        await asyncio.sleep(0.1)
        return None

    def is_pressed(self, button: Button) -> bool:
        """Check if a button is currently pressed."""
        return False  # Stub

    def close(self):
        """Release GPIO resources."""
        self._initialized = False
        logger.info("Button handler closed")
