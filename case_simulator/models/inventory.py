from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Tuple

from case_simulator.models.item import Item
from case_simulator.models.case import Case


@dataclass
class Inventory:
    """Инвентарь игрока: хранит количество кейсов и предметов + каталоги."""

    item_counts: Dict[str, int] = field(default_factory=dict)
    case_counts: Dict[str, int] = field(default_factory=dict)
    item_catalog: Dict[str, Item] = field(default_factory=dict)
    case_catalog: Dict[str, Case] = field(default_factory=dict)

    # --- Мутации каталога/количеств ---
    def register_item(self, item: Item) -> None:
        self.item_catalog[item.id] = item

    def register_case(self, case: Case) -> None:
        self.case_catalog[case.id] = case

    def add_item(self, item: Item, qty: int = 1) -> None:
        self.register_item(item)
        self.item_counts[item.id] = self.item_counts.get(item.id, 0) + max(0, qty)

    def add_case(self, case: Case, qty: int = 1) -> None:
        self.register_case(case)
        self.case_counts[case.id] = self.case_counts.get(case.id, 0) + max(0, qty)

    def remove_case(self, case: Case, qty: int = 1) -> bool:
        """Потратить/удалить кейсы из инвентаря. Возвращает успех операции."""
        if qty <= 0:
            return True
        current = self.case_counts.get(case.id, 0)
        if current >= qty:
            self.case_counts[case.id] = current - qty
            return True
        return False

    def remove_item(self, item: Item, qty: int = 1) -> bool:
        """Удалить указанное количество предметов из инвентаря. Возвращает True при успехе."""
        if qty <= 0:
            return True
        current = self.item_counts.get(item.id, 0)
        if current >= qty:
            self.item_counts[item.id] = current - qty
            return True
        return False

    # --- Чтение ---
    def get_items(self) -> List[Tuple[Item, int]]:
        result: List[Tuple[Item, int]] = []
        for item_id, count in self.item_counts.items():
            item = self.item_catalog.get(item_id)
            if item and count > 0:
                result.append((item, count))
        return result

    def get_cases(self) -> List[Tuple[Case, int]]:
        result: List[Tuple[Case, int]] = []
        for case_id, count in self.case_counts.items():
            case = self.case_catalog.get(case_id)
            if case and count > 0:
                result.append((case, count))
        return result
