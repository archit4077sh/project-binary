"""
human_simulator.py — OS-level keyboard automation using pyautogui.
Simulates human typing with variable keystroke delays and natural pauses.
"""

import time
import random
import sys
import pyautogui

from config import (
    TYPING_DELAY_MIN,
    TYPING_DELAY_MAX,
    PUNCTUATION_PAUSE_MIN,
    PUNCTUATION_PAUSE_MAX,
    THINKING_PAUSE_MIN,
    THINKING_PAUSE_MAX,
    THINKING_PAUSE_PROBABILITY,
    WAIT_MIN_SECONDS,
    WAIT_MAX_SECONDS,
)

# Characters that trigger a longer post-character pause
PUNCTUATION_CHARS = set(".,;:!?")

# pyautogui safety: disable fail-safe (moving mouse to corner won't abort)
# Comment this out if you want the fail-safe enabled:
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0  # we manage delays ourselves


def type_humanly(text: str) -> None:
    """
    Type `text` character-by-character with human-like timing:
    - Random 30-120ms delay per character
    - 200-600ms pause after punctuation
    - Random 500-1500ms 'thinking' pause at ~4% of spaces
    - Newlines (\\n) are sent as Shift+Enter to avoid premature submission
    - Only press_enter() at the end sends the bare Enter to submit
    """
    for char in text:
        if char == "\n":
            # Shift+Enter = new line without submitting (works in ChatGPT, Claude, Gemini)
            pyautogui.hotkey("shift", "enter")
            delay = random.uniform(0.08, 0.20)
        elif char == "`":
            # pyautogui.write can't type backticks reliably on some keyboards
            pyautogui.hotkey("shift", "grave") if False else _type_char(char)
            delay = random.uniform(TYPING_DELAY_MIN, TYPING_DELAY_MAX)
        else:
            _type_char(char)
            # Determine post-char delay
            if char in PUNCTUATION_CHARS:
                delay = random.uniform(PUNCTUATION_PAUSE_MIN, PUNCTUATION_PAUSE_MAX)
            elif char == " " and random.random() < THINKING_PAUSE_PROBABILITY:
                delay = random.uniform(THINKING_PAUSE_MIN, THINKING_PAUSE_MAX)
            else:
                delay = random.uniform(TYPING_DELAY_MIN, TYPING_DELAY_MAX)

        time.sleep(delay)


def _type_char(char: str) -> None:
    """Type a single character, with a unicode-safe fallback via clipboard paste."""
    try:
        pyautogui.write(char, interval=0)
    except Exception:
        # For characters pyautogui can't write directly, use clipboard paste
        import pyperclip  # optional fast-path, ignored if not installed
        try:
            pyperclip.copy(char)
            pyautogui.hotkey("ctrl", "v")
        except Exception:
            pass  # silently skip truly un-typeable chars


def press_enter() -> None:
    """Press the Enter key to submit the message."""
    time.sleep(random.uniform(0.3, 0.7))  # brief pause before submitting
    pyautogui.press("enter")


def countdown(seconds: int) -> None:
    """
    Print a countdown so the user has time to click into the chat input.
    Displays a live countdown in the terminal.
    """
    print(f"\n[WAIT] You have {seconds} seconds to click into the chat input box...")
    for remaining in range(seconds, 0, -1):
        sys.stdout.write(f"\r   > Starting in {remaining:2d} seconds...  ")
        sys.stdout.flush()
        time.sleep(1)
    sys.stdout.write("\r   > Typing now!                    \n\n")
    sys.stdout.flush()


def random_idle(min_seconds: int = WAIT_MIN_SECONDS, max_seconds: int = WAIT_MAX_SECONDS) -> None:
    """
    Wait a random duration between questions.
    Displays a live countdown in the terminal so the user knows what's happening.
    """
    wait = random.randint(min_seconds, max_seconds)
    minutes, seconds = divmod(wait, 60)
    print(f"\n[IDLE] Waiting {minutes}m {seconds}s before next question...")

    for remaining in range(wait, 0, -1):
        m, s = divmod(remaining, 60)
        sys.stdout.write(f"\r   Next question in: {m:02d}:{s:02d}  ")
        sys.stdout.flush()
        time.sleep(1)

    sys.stdout.write("\r                              \n")
    sys.stdout.flush()
