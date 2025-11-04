from __future__ import annotations

import os
import sys
from typing import Final


class Console:
    """Utility wrapper around console operations."""

    _CLEAR_COMMAND_WINDOWS: Final[str] = "cls"
    _CLEAR_COMMAND_UNIX: Final[str] = "clear"

    def clear(self) -> None:
        """Clear the console screen based on underlying OS."""
        command = self._CLEAR_COMMAND_WINDOWS if os.name == "nt" else self._CLEAR_COMMAND_UNIX
        os.system(command)

    def write_line(self, text: str = "") -> None:
        print(text)

    def write_empty_line(self) -> None:
        print()

    def read_input(self, prompt: str = "") -> str:
        return input(prompt)

    def wait_for_key(self, message: str | None = None) -> None:
        """Wait for Enter or Escape key press."""
        prompt = message or "Нажмите Enter или Esc для продолжения..."
        try:
            if os.name == "nt":  # Windows
                import msvcrt
                print(prompt, end="", flush=True)
                while True:
                    if msvcrt.kbhit():
                        key = msvcrt.getch()
                        # Enter (13), Escape (27) или Space (32)
                        if key in (b'\r', b'\x1b', b' '):
                            print()  # Новая строка после нажатия
                            break
            else:  # Unix/Linux/Mac
                import tty
                import termios
                print(prompt, end="", flush=True)
                fd = sys.stdin.fileno()
                old_settings = termios.tcgetattr(fd)
                try:
                    tty.setraw(fd)
                    key = sys.stdin.read(1)
                    # Enter (10), Escape (27) или Space (32)
                    if ord(key) in (10, 27, 32):
                        print()
                finally:
                    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        except (EOFError, KeyboardInterrupt):
            print()
            sys.exit(0)

    def wait_for_enter(self, message: str | None = None) -> None:
        """Backward compatibility: redirect to wait_for_key."""
        self.wait_for_key(message)
