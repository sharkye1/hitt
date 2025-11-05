from __future__ import annotations

from typing import Iterable, List, Optional, Tuple

from case_simulator.scenes.base import Scene
from case_simulator.data import presets
from case_simulator.models.item import Item


class InventoryScene(Scene):
    """Console-based inventory viewer.

    Features:
    - Two main sections: Cases и Items
    - Item subcategories: pistols, rifles, snipers, knives, all
    - Sorting: by price or by rare (ascending/descending)
    """

    ITEM_CATEGORIES = ["all", "pistol", "rifle", "sniper", "knife"]
    SORT_FIELDS = ["price", "rare"]

    def _filter_items(self, items: Iterable[Item], category: str) -> List[Item]:
        if category == "all":
            return list(items)
        return [i for i in items if i.category == category]

    def _sort_items(self, items: List[Item], field: str, reverse: bool) -> List[Item]:
        key = (lambda x: getattr(x, field, 0)) if field in self.SORT_FIELDS else (lambda x: x.price)
        return sorted(items, key=key, reverse=reverse)

    def _display_items_table(self, items: List[Item]) -> None:
        self.console.write_line("ID | Name | Category | Rare | Price")
        self.console.write_line("---+------+----------+------+------")
        for it in items:
            self.console.write_line(f"{it.id} | {it.name} | {it.category} | {it.rare} | {it.price}")

    def run(self) -> Optional[str]:
        # prepare data
        all_items = list(presets.ITEMS)
        all_cases = list(presets.CASES)

        category_idx = 0
        sort_field = "price"
        sort_reverse = False
        view_mode = "items"  # or "cases"

        while True:
            self.console.clear()
            self.console.write_line("=== Инвентарь ===")
            self.console.write_line(f"Баланс: {self.state.balance}")
            self.console.write_line("")

            self.console.write_line(f"Текущий режим: {view_mode}")
            self.console.write_line("[T] Переключить режим (Items/Cases)")
            self.console.write_line("[C] Изменить категорию (для Items): " + ", ".join(self.ITEM_CATEGORIES))
            self.console.write_line("[S] Сортировка: поле=" + sort_field + (", desc" if sort_reverse else ", asc"))
            self.console.write_line("[O] Изменить порядок сортировки (asc/desc)")
            self.console.write_line("[B] Назад в меню")
            self.console.write_empty_line()

            if view_mode == "items":
                cat = self.ITEM_CATEGORIES[category_idx]
                filtered = self._filter_items(all_items, cat)
                sorted_items = self._sort_items(filtered, sort_field, sort_reverse)
                self._display_items_table(sorted_items)
            else:
                # display cases
                self.console.write_line("ID | Name | Price | Contains count")
                self.console.write_line("---+------+-------+---------------")
                for c in all_cases:
                    contains = len(c.items)
                    self.console.write_line(f"{c.id} | {c.name} | {c.price} | {contains}")

            choice = self.console.read_input("Введите команду (T/C/S/O/B): ").strip().lower()
            if choice == "t":
                view_mode = "cases" if view_mode == "items" else "items"
            elif choice == "c":
                # only relevant for items
                if view_mode == "items":
                    category_idx = (category_idx + 1) % len(self.ITEM_CATEGORIES)
            elif choice == "s":
                # cycle sort field
                idx = self.SORT_FIELDS.index(sort_field) if sort_field in self.SORT_FIELDS else 0
                idx = (idx + 1) % len(self.SORT_FIELDS)
                sort_field = self.SORT_FIELDS[idx]
            elif choice == "o":
                sort_reverse = not sort_reverse
            elif choice == "b":
                return "menu"
            else:
                self.console.write_line("Неизвестная команда")
                self.console.wait_for_key("Нажмите Enter для продолжения...")
