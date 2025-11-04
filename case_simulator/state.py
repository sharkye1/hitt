from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from case_simulator.models.inventory import Inventory


@dataclass
class GameState:
    """Единое состояние игры/сессии."""

    inventory: Inventory
    balance: int = 0
    # Список id префабов/пресетов, уже выданных игроку (чтобы не выдавать их повторно)
    granted_presets: List[str] = field(default_factory=list)

    # Баланс (депозит)
    def add_balance(self, amount: int) -> None:
        if amount <= 0:
            return
        self.balance += amount

    def try_deduct(self, amount: int) -> bool:
        if amount < 0:
            return False
        if self.balance >= amount:
            self.balance -= amount
            return True
        return False
