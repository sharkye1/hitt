from __future__ import annotations

from typing import Iterable, List, Optional, Tuple

from case_simulator.scenes.base import Scene
from case_simulator.data import presets
from case_simulator.models.item import Item


class InventoryScene(Scene):
    """Класс для отображения инвентаря игрока.

    Включает в себя:
    - Две основные секции: Кейсы и Предметы
    - Подкатегории предметов: пистолеты, винтовки, снайперы, ножи, все
    - Сортировка: по цене или по редкости (по возрастанию/убыванию)
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
        # compute column widths
        id_w = max((len(str(it.id)) for it in items), default=2)
        name_w = max((len(str(it.name)) for it in items), default=4)
        cat_w = max((len(str(it.category)) for it in items), default=8)
        rare_w = max((len(str(it.rare)) for it in items), default=4)
        price_w = max((len(str(it.price)) for it in items), default=5)

        hdr = f"{'ID'.ljust(id_w)} | {'Name'.ljust(name_w)} | {'Category'.ljust(cat_w)} | {'Rare'.rjust(rare_w)} | {'Price'.rjust(price_w)}"
        sep = f"{'-' * id_w}-+-{'-' * name_w}-+-{'-' * cat_w}-+-{'-' * rare_w}-+-{'-' * price_w}"
        self.console.write_line(hdr)
        self.console.write_line(sep)

        for it in items:
            line = (
                f"{str(it.id).ljust(id_w)} | "
                f"{str(it.name).ljust(name_w)} | "
                f"{str(it.category).ljust(cat_w)} | "
                f"{str(it.rare).rjust(rare_w)} | "
                f"{str(it.price).rjust(price_w)}"
            )
            self.console.write_line(line)

    def run(self) -> Optional[str]:
        # prepare data
        all_items = list(presets.ITEMS)
        all_cases = list(presets.CASES)
        category_idx = 0
        sort_field = "price"
        sort_reverse = False
        # Modes:
        # - "simple" : initial owned-items/simple view
        # - "advanced_items": advanced view for owned items (filters/sort)
        # - "advanced_cases": advanced view for owned cases
        # - "catalog_items": browse full catalog of items (no counts)
        # - "catalog_cases": browse full catalog of cases
        view_mode = "simple"

        while True:
            self.console.clear()
            self.console.write_line("=== Инвентарь ===")
            self.console.write_line(f"Баланс: {self.state.balance}")
            self.console.write_line("")

            # Header actions help (commands vary by mode - shown below)
            self.console.write_line(f"Текущий режим: {view_mode}")
            self.console.write_line("(A) Продвинутый режим | (V) Просмотр каталога | (q) Назад")
            self.console.write_line("")
            self.console.write_empty_line()

            if view_mode == "advanced_items":
                # advanced items: show only owned items with filters/sort
                owned = self.state.inventory.get_items()
                if not owned:
                    self.console.write_line("Инвентарь пуст. У вас нет предметов.")
                else:
                    # apply category filter
                    cat = self.ITEM_CATEGORIES[category_idx]
                    filtered = [(it, cnt) for it, cnt in owned if cat == "all" or it.category == cat]
                    # sort by selected field
                    sorted_items = sorted(filtered, key=lambda ic: getattr(ic[0], sort_field), reverse=sort_reverse)

                    price_w = max((len(str(it.price)) for it, _ in sorted_items), default=5)
                    cnt_w = max((len(str(cnt)) for _, cnt in sorted_items), default=3)
                    name_w = max((len(str(it.name)) for it, _ in sorted_items), default=4)
                    id_w = max((len(str(it.id)) for it, _ in sorted_items), default=2)

                    hdr = f"{'Price'.rjust(price_w)} | {'Qty'.rjust(cnt_w)} | {'Name'.ljust(name_w)} | {'ID'.ljust(id_w)}"
                    sep = f"{'-' * price_w}-+-{'-' * cnt_w}-+-{'-' * name_w}-+-{'-' * id_w}"
                    self.console.write_line(hdr)
                    self.console.write_line(sep)
                    for it, cnt in sorted_items:
                        self.console.write_line(
                            f"{str(it.price).rjust(price_w)} | {str(cnt).rjust(cnt_w)} | {str(it.name).ljust(name_w)} | {str(it.id).ljust(id_w)}"
                        )
                # help for advanced items
                self.console.write_line("")
                self.console.write_line("[T] Переключить на кейсы | [C] Сменить категорию | [S] Сменить поле сортировки | [O] Порядок | [V] Посмотреть каталог | [pN] Продать предмет N | [q] Назад")
            elif view_mode == "catalog_items":
                # full catalog browsing (no counts)
                sorted_by_price = self._sort_items(all_items, sort_field, sort_reverse)
                # compute widths
                price_w = max((len(str(it.price)) for it in sorted_by_price), default=5)
                name_w = max((len(str(it.name)) for it in sorted_by_price), default=4)
                id_w = max((len(str(it.id)) for it in sorted_by_price), default=2)

                hdr = f"{'Price'.rjust(price_w)} | {'Name'.ljust(name_w)} | {'ID'.ljust(id_w)}"
                sep = f"{'-' * price_w}-+-{'-' * name_w}-+-{'-' * id_w}"
                self.console.write_line(hdr)
                self.console.write_line(sep)
                for it in sorted_by_price:
                    self.console.write_line(f"{str(it.price).rjust(price_w)} | {str(it.name).ljust(name_w)} | {str(it.id).ljust(id_w)}")
                self.console.write_line("")
                self.console.write_line("[V] Вернуться к продвинутому режиму | [q] Назад")
            elif view_mode == "simple":
                # simple view: list only items actually owned by the player,
                # sorted by price ascending
                owned = self.state.inventory.get_items()  # List[Tuple[Item,int]]
                if not owned:
                    self.console.write_line("Инвентарь пуст. У вас нет предметов.")
                else:
                    owned_sorted = sorted(owned, key=lambda ic: ic[0].price)
                    price_w = max((len(str(it.price)) for it, _ in owned_sorted), default=5)
                    cnt_w = max((len(str(cnt)) for _, cnt in owned_sorted), default=3)
                    name_w = max((len(str(it.name)) for it, _ in owned_sorted), default=4)
                    id_w = max((len(str(it.id)) for it, _ in owned_sorted), default=2)

                    hdr = f"{'Price'.rjust(price_w)} | {'Qty'.rjust(cnt_w)} | {'Name'.ljust(name_w)} | {'ID'.ljust(id_w)}"
                    sep = f"{'-' * price_w}-+-{'-' * cnt_w}-+-{'-' * name_w}-+-{'-' * id_w}"
                    self.console.write_line(hdr)
                    self.console.write_line(sep)
                    for it, cnt in owned_sorted:
                        self.console.write_line(
                            f"{str(it.price).rjust(price_w)} | {str(cnt).rjust(cnt_w)} | {str(it.name).ljust(name_w)} | {str(it.id).ljust(id_w)}"
                        )
                self.console.write_line("")
                self.console.write_line("[A] Открыть продвинутый режим")
                self.console.write_line("[V] Просмотреть каталог (все предметы)")
                self.console.write_line("[pN] Продать предмет N (например p1) | [q] Назад в меню")
            elif view_mode == "advanced_cases":
                owned_cases = self.state.inventory.get_cases()
                if not owned_cases:
                    self.console.write_line("У вас нет кейсов.")
                else:
                    id_w = max((len(str(c.id)) for c, _ in owned_cases), default=2)
                    name_w = max((len(str(c.name)) for c, _ in owned_cases), default=4)
                    price_w = max((len(str(c.price)) for c, _ in owned_cases), default=5)
                    cnt_w = max((len(str(cnt)) for _, cnt in owned_cases), default=3)

                    hdr = f"{'ID'.ljust(id_w)} | {'Name'.ljust(name_w)} | {'Price'.rjust(price_w)} | {'Qty'.rjust(cnt_w)}"
                    sep = f"{'-' * id_w}-+-{'-' * name_w}-+-{'-' * price_w}-+-{'-' * cnt_w}"
                    self.console.write_line(hdr)
                    self.console.write_line(sep)
                    for c, cnt in owned_cases:
                        self.console.write_line(
                            f"{str(c.id).ljust(id_w)} | {str(c.name).ljust(name_w)} | {str(c.price).rjust(price_w)} | {str(cnt).rjust(cnt_w)}"
                        )
                self.console.write_line("")
                self.console.write_line("[T] Переключить на предметы | [V] Просмотреть все кейсы | [q] Назад")
            elif view_mode == "catalog_cases":
                # show full list of cases
                id_w = max((len(str(c.id)) for c in all_cases), default=2)
                name_w = max((len(str(c.name)) for c in all_cases), default=4)
                price_w = max((len(str(c.price)) for c in all_cases), default=5)
                contains_w = max((len(str(len(c.items))) for c in all_cases), default=6)

                hdr = f"{'ID'.ljust(id_w)} | {'Name'.ljust(name_w)} | {'Price'.rjust(price_w)} | {'Contains'.rjust(contains_w)}"
                sep = f"{'-' * id_w}-+-{'-' * name_w}-+-{'-' * price_w}-+-{'-' * contains_w}"
                self.console.write_line(hdr)
                self.console.write_line(sep)
                for c in all_cases:
                    contains = len(c.items)
                    self.console.write_line(
                        f"{str(c.id).ljust(id_w)} | {str(c.name).ljust(name_w)} | {str(c.price).rjust(price_w)} | {str(contains).rjust(contains_w)}"
                    )
                self.console.write_line("")
                self.console.write_line("[V] Вернуться к продвинутому режиму кейсов | [q] Назад")

            # adapt prompt to current mode
            if view_mode == "simple":
                prompt = "Введите команду (A/V/q): "
            elif view_mode == "advanced_items":
                prompt = "Введите команду (T/C/S/O/V/q): "
            elif view_mode == "catalog_items":
                prompt = "Введите команду (V/q): "
            elif view_mode == "advanced_cases":
                prompt = "Введите команду (T/V/q): "
            elif view_mode == "catalog_cases":
                prompt = "Введите команду (V/q): "
            else:
                prompt = "Введите команду (q): "

            choice = self.console.read_input(prompt).strip().lower()

            # handle commands
            if choice == "a":
                # to advanced items
                view_mode = "advanced_items"
            elif choice == "v":
                # toggle between catalog and advanced for current axis
                if view_mode == "catalog_items":
                    view_mode = "advanced_items"
                elif view_mode == "catalog_cases":
                    view_mode = "advanced_cases"
                elif view_mode in ("simple", "advanced_items"):
                    view_mode = "catalog_items"
                else:
                    view_mode = "catalog_cases"
            elif choice == "t":
                # toggle between items and cases (respecting advanced/catalog)
                if view_mode in ("advanced_items", "catalog_items"):
                    # go to cases equivalent
                    view_mode = "advanced_cases" if view_mode == "advanced_items" else "catalog_cases"
                elif view_mode in ("advanced_cases", "catalog_cases"):
                    view_mode = "advanced_items" if view_mode == "advanced_cases" else "catalog_items"
            elif choice == "c":
                if view_mode == "advanced_items":
                    category_idx = (category_idx + 1) % len(self.ITEM_CATEGORIES)
            # Selling command: p<number> or s<number>
            elif choice.startswith(("p", "s")):
                # Only allow selling when we are showing owned items (simple or advanced_items)
                if view_mode not in ("simple", "advanced_items"):
                    self.console.write_line("Продажа доступна только для списка owned items.")
                    self.console.wait_for_key()
                else:
                    numpart = choice[1:]
                    if not numpart.isdigit():
                        self.console.write_line("Укажите номер предмета, например p1")
                        self.console.wait_for_key()
                    else:
                        idx = int(numpart) - 1
                        owned_list = self.state.inventory.get_items()
                        if not owned_list:
                            self.console.write_line("У вас нет предметов для продажи.")
                            self.console.wait_for_key()
                        else:
                            # Determine which list is being shown and compute ordering
                            if view_mode == "simple":
                                ordered = sorted(owned_list, key=lambda ic: ic[0].price)
                            else:
                                # advanced_items uses category filter and sort_field
                                cat = self.ITEM_CATEGORIES[category_idx]
                                filtered = [(it, cnt) for it, cnt in owned_list if cat == "all" or it.category == cat]
                                ordered = sorted(filtered, key=lambda ic: getattr(ic[0], sort_field), reverse=sort_reverse)

                            if idx < 0 or idx >= len(ordered):
                                self.console.write_line("Нет такого номера предмета.")
                                self.console.wait_for_key()
                            else:
                                it, cnt = ordered[idx]
                                sell_price = int(it.price * 0.8)
                                # confirm
                                # allow single-key confirmation (y/n) without Enter
                                try:
                                    confirm = self.console.read_key(f"Продать {it.name} за {sell_price}? (y/n): ").strip().lower()
                                except Exception:
                                    confirm = self.console.read_input(f"Продать {it.name} за {sell_price}? (y/n): ").strip().lower()
                                if confirm == "y":
                                    ok = self.state.inventory.remove_item(it, qty=1)
                                    if ok:
                                        self.state.add_balance(sell_price)
                                        self.console.write_line(f"Продано: {it.name}. Баланс: {self.state.balance}")
                                    else:
                                        self.console.write_line("Не удалось продать: недостаточно штук.")
                                    self.console.wait_for_key()
            elif choice == "s":
                if view_mode in ("advanced_items", "catalog_items"):
                    idx = self.SORT_FIELDS.index(sort_field) if sort_field in self.SORT_FIELDS else 0
                    idx = (idx + 1) % len(self.SORT_FIELDS)
                    sort_field = self.SORT_FIELDS[idx]
            elif choice == "o":
                sort_reverse = not sort_reverse
            elif choice in ("b", "q"):
                return "menu"
            else:
                self.console.write_line("Неизвестная команда")
                self.console.wait_for_key("Нажмите Enter для продолжения...")
