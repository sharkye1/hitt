from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from case_simulator.utils.console import Console
from case_simulator.state import GameState


class Scene(ABC):
    """Базовый класс для всех сцен симулятора."""
    def __init__(self, console: Console, state: GameState) -> None:
        self.console = console
        self.state = state

    @abstractmethod
    def run(self) -> Optional[str]:
        """Выполнить логику сцены и вернуть имя следующей сцены."""
        raise NotImplementedError
