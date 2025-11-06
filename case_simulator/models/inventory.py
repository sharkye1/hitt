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
    # Per-instance qualities for items owned by the player. Keys are item ids
    # and values are lists of float qualities (0.0..1.0, 1.0 excluded). This
    # allows storing different qualities for multiple copies of the same item.
    item_qualities: Dict[str, List[float]] = field(default_factory=dict)

    # --- Мутации каталога/количеств ---
    def register_item(self, item: Item) -> None:
        # Register template item only if not already present. We avoid
        # overwriting the catalog entry because runtime instances of Item may
        # carry per-instance `quality` values and should not replace the
        # canonical template stored in the catalog.
        if item.id not in self.item_catalog:
            self.item_catalog[item.id] = item

    def register_case(self, case: Case) -> None:
        self.case_catalog[case.id] = case

    def add_item(self, item: Item, qty: int = 1, quality: float | None = None) -> None:
        """Add `qty` copies of `item` to the inventory.

        If `quality` is provided, it will be recorded as per-instance
        qualities for this item id (appended `qty` times). Otherwise the
        item is treated as a generic/template copy.
        """
        self.register_item(item)
        self.item_counts[item.id] = self.item_counts.get(item.id, 0) + max(0, qty)

        if quality is not None:
            lst = self.item_qualities.setdefault(item.id, [])
            for _ in range(max(0, qty)):
                lst.append(float(quality))

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
            # Also remove per-instance qualities for the removed copies if we
            # have stored qualities. We pop from the end (LIFO) which matches
            # last-added semantics used when items are added with quality.
            qlist = self.item_qualities.get(item.id)
            if qlist and len(qlist) > 0:
                remove_n = min(qty, len(qlist))
                for _ in range(remove_n):
                    qlist.pop()
                if len(qlist) == 0:
                    # remove empty list to keep serialization compact
                    self.item_qualities.pop(item.id, None)
            return True
        return False

    def remove_item_by_quality(self, item_id: str, quality: float) -> bool:
        """Remove a single copy of item `item_id` that has the specified
        `quality`. Returns True if an instance was removed.

        If an exact match isn't found, removes the closest quality (by
        absolute difference). The item_counts is decremented accordingly.
        """
        current = self.item_counts.get(item_id, 0)
        if current <= 0:
            return False

        qlist = self.item_qualities.get(item_id)
        if not qlist:
            # No per-instance qualities — fall back to removing generic copy
            # by reducing item_counts.
            self.item_counts[item_id] = current - 1
            return True

        # find index of closest quality
        closest_idx = 0
        closest_diff = abs(qlist[0] - quality)
        for i, q in enumerate(qlist):
            d = abs(q - quality)
            if d < closest_diff:
                closest_diff = d
                closest_idx = i

        # remove that quality entry
        qlist.pop(closest_idx)
        if len(qlist) == 0:
            self.item_qualities.pop(item_id, None)

        # decrement item count
        self.item_counts[item_id] = current - 1
        return True

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

    # --- Helpers for qualities ---
    def get_item_qualities(self, item_id: str) -> List[float]:
        """Return the list of qualities for owned instances of `item_id`.

        The returned list may be empty even if `item_counts[item_id]` > 0 if
        some copies were added without quality metadata.
        """
        return list(self.item_qualities.get(item_id, []))
