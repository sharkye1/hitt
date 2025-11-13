from __future__ import annotations

from typing import Optional, List, Tuple, Any

from case_simulator.scenes.base import Scene
from case_simulator.models.case import Case
from case_simulator.models.item import Item
from case_simulator.data import presets


class ShopScene(Scene):
    """Simple shop: buy cases and items with in-game balance."""

    def run(self) -> Optional[str]:
        while True:
            self.console.clear()
            self.console.write_line("=== Магазин ===")
            self.console.write_line(f"Баланс: {self.state.balance}")
            self.console.write_empty_line()

            cases = self._list_cases()
            items = self._list_items()

            self.console.write_line("Кейсы:")
            for idx, (case_id, case, price, stock) in enumerate(cases, start=1):
                stock_text = f" [{stock} в наличии]" if isinstance(stock, int) else ""
                self.console.write_line(f"  C{idx}. {case.name} — {price} монет{stock_text}")
            if not cases:
                self.console.write_line("  (нет доступных кейсов)")

            self.console.write_empty_line()
            self.console.write_line("Предметы:")
            for idx, (item_id, item, price, stock) in enumerate(items, start=1):
                stock_text = f" [{stock} в наличии]" if isinstance(stock, int) else ""
                self.console.write_line(f"  I{idx}. {item.name} (id={item_id}) — {price} монет{stock_text}")
            if not items:
                self.console.write_line("  (нет доступных предметов)")

            self.console.write_empty_line()
            self.console.write_line("Выберите то, что хотите купить:")
            self.console.write_line("  Формат: C1 или I2 (например C1 купить кейс #1).")
            self.console.write_line("  B - пополнить баланс, q - назад в меню")

            # Try single-key entry first (for selecting numbered cases quickly).
            # If the key is a letter command like 'C' or 'I', read the rest of the
            # line with read_input so the user can type 'C1' or 'I2' and press Enter.
            try:
                first = self.console.read_key("Ваш выбор: ")
            except Exception:
                first = self.console.read_input("Ваш выбор: ")
            if first is None:
                first = ""
            first = first.strip()
            if not first:
                continue

            # Quit/top-up
            if first.lower() == "q":
                return "menu"
            if first.upper() == "B":
                self._top_up()
                continue

            choice = None
            # If first char is a letter command that expects a number (C/I),
            # read the rest of the line to allow 'C1' typed then Enter.
            if len(first) == 1 and first.upper() in ("C", "I"):
                rest = ""
                try:
                    # read_input will consume the rest of the line (if the user
                    # typed 'C1' and pressed Enter, this returns '1') or block
                    # for further input.
                    rest = self.console.read_input("")
                except Exception:
                    rest = ""
                choice = (first + (rest or "")).strip()
            else:
                # If user pressed a digit (single-key), treat as quick case selection;
                # otherwise use the full token entered.
                if len(first) == 1 and first.isdigit():
                    choice = first
                else:
                    choice = first

            if not choice:
                continue

            # Parse purchase
            if choice[0].upper() == "C":
                try:
                    num = int(choice[1:]) - 1
                    # cases entries: (case_id, Case, price, stock)
                    case_id, case, price, stock = cases[num]
                except Exception:
                    self.console.write_line("Неверный код кейса. Попробуйте снова.")
                    self.console.wait_for_key()
                    continue
                self._attempt_purchase_case(case, price, case_id)
                continue

            if choice[0].upper() == "I":
                try:
                    num = int(choice[1:]) - 1
                    # items entries: (item_id, Item, price, stock)
                    item_id, item, price, stock = items[num]
                except Exception:
                    self.console.write_line("Неверный код предмета. Попробуйте снова.")
                    self.console.wait_for_key()
                    continue
                self._attempt_purchase_item(item, price, item_id)
                continue

            self.console.write_line("Неизвестный вариант. Попробуйте снова.")
            self.console.wait_for_key()


    def _list_cases(self) -> List[Tuple[str, Case, int, Any]]:
        # Возвращаем список (case_id, Case, price, stock) по SHOP_STOCK
        result: List[Tuple[str, Case, int, Any]] = []
        for obj_id, meta in presets.SHOP_STOCK.items():
            if meta.get("type") != "case":
                continue
            case = self.state.inventory.case_catalog.get(obj_id)
            if not case:
                # если объект не зарегистрирован в каталоге — пропускаем
                continue
            price = meta.get("price", case.price)
            stock = meta.get("stock")
            result.append((obj_id, case, price, stock))
        # Сортируем кейсы от дешёвых к дорогим по цене в магазине
        result.sort(key=lambda x: x[2])
        return result

    def _list_items(self) -> List[Tuple[str, Item, int, Any]]:
        result: List[Tuple[str, Item, int, Any]] = []
        for obj_id, meta in presets.SHOP_STOCK.items():
            if meta.get("type") != "item":
                continue
            item = self.state.inventory.item_catalog.get(obj_id)
            if not item:
                continue
            price = meta.get("price", item.price)
            stock = meta.get("stock")
            result.append((obj_id, item, price, stock))
        return result

    def _attempt_purchase_case(self, case: Case, price: int, shop_id: str | None = None) -> None:
        if not self.state.try_deduct(price):
            self.console.write_line("Недостаточно средств.")
            self.console.wait_for_key()
            return

        # Добавляем кейс в инвентарь
        self.state.inventory.add_case(case, qty=1)

        # Уменьшаем запас в магазине (в памяти), если он ограничен
        if shop_id:
            meta = presets.SHOP_STOCK.get(shop_id)
            if isinstance(meta, dict) and isinstance(meta.get("stock"), int):
                if meta["stock"] > 0:
                    meta["stock"] -= 1

        self.console.write_line(f"Куплено: {case.name} за {price} монет.")
        self.console.wait_for_key()

    def _attempt_purchase_item(self, item: Item, price: int, shop_id: str | None = None) -> None:
        if not self.state.try_deduct(price):
            self.console.write_line("Недостаточно средств.")
            self.console.wait_for_key()
            return

        self.state.inventory.add_item(item, qty=1)

        # Уменьшаем запас в магазине (в памяти), если он ограничен
        if shop_id:
            meta = presets.SHOP_STOCK.get(shop_id)
            if isinstance(meta, dict) and isinstance(meta.get("stock"), int):
                if meta["stock"] > 0:
                    meta["stock"] -= 1

        self.console.write_line(f"Куплено: {item.name} за {price} монет.")
        self.console.wait_for_key()

    def _top_up(self) -> None:
        v = self.console.read_input("Сколько добавить на баланс (целое число): ")
        try:
            n = int(v)
            if n <= 0:
                raise ValueError()
        except Exception:
            self.console.write_line("Некорректное значение.")
            self.console.wait_for_key()
            return
        self.state.add_balance(n)
        self.console.write_line(f"Баланс пополнен на {n}.")
        self.console.wait_for_key()
