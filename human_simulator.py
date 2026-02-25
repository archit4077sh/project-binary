"""
human_simulator.py — OS-level keyboard automation using pyautogui + pyperclip.
Uses clipboard paste for instant question delivery instead of char-by-char typing.
"""

import time
import random
import sys
import pyautogui
import pyperclip

from config import (
    WAIT_MIN_SECONDS,
    WAIT_MAX_SECONDS,
)

# pyautogui safety
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0

# Saved position of the chat input box — captured during countdown
_INPUT_POS: tuple[int, int] | None = None


def type_humanly(text: str) -> None:
    """
    Paste `text` instantly via the clipboard.

    The question is split on newlines. Each line is copied to the clipboard
    and pasted with Ctrl+V. Between lines, Shift+Enter inserts a newline
    without submitting. This avoids slow char-by-char typing entirely.
    """
    lines = text.split("\n")
    for i, line in enumerate(lines):
        # Copy line to clipboard and paste it
        pyperclip.copy(line)
        pyautogui.hotkey("ctrl", "v")
        time.sleep(0.05)  # tiny settle time after paste

        if i < len(lines) - 1:
            # Shift+Enter = newline without submitting
            pyautogui.hotkey("shift", "enter")
            time.sleep(0.05)


def press_enter() -> None:
    """Press the Enter key to submit the message."""
    time.sleep(random.uniform(0.3, 0.7))  # brief pause before submitting
    pyautogui.press("enter")


def countdown(seconds: int) -> None:
    """
    Print a countdown so the user has time to click into the chat input.
    Captures the mouse position at the end so we can re-click it automatically.
    """
    global _INPUT_POS
    print(f"\n[WAIT] You have {seconds} seconds to click into the chat input box...")
    for remaining in range(seconds, 0, -1):
        sys.stdout.write(f"\r   > Starting in {remaining:2d} seconds...  ")
        sys.stdout.flush()
        time.sleep(1)
    # Snapshot the cursor position — user should be hovering over / inside the input now
    _INPUT_POS = pyautogui.position()
    sys.stdout.write(f"\r   > Typing now! (input locked at {_INPUT_POS.x},{_INPUT_POS.y})   \n\n")
    sys.stdout.flush()


def click_input() -> None:
    """
    Click the saved input box position to re-focus it.
    Called automatically before every question after the first.
    """
    if _INPUT_POS is None:
        return  # no position saved yet (e.g. dry-run)
    time.sleep(random.uniform(0.3, 0.6))  # small natural delay before clicking
    pyautogui.click(_INPUT_POS.x, _INPUT_POS.y)
    time.sleep(random.uniform(0.2, 0.4))  # let the UI register the focus


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
