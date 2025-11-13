from __future__ import annotations

from typing import Optional, List, Tuple

from case_simulator.scenes.base import Scene
from case_simulator.utils.crafting import craft_items, TIERS
from case_simulator.utils.pricing import price_multiplier
from case_simulator.models.item import Item
from case_simulator.data import presets


class CraftingScene(Scene):
    """Interactive crafting scene.

    Modes supported:
      - probabilistic: user picks 2..8 weapons and a success tier (50/35/25/10)
      - deterministic: merge items deterministically
      - fusion: combine items (quality averaged)
      - upgrade: attempt to upgrade a single item

    Per your spec, selected input items are burned on attempt. The new item
    receives a freshly generated quality (not inherited), which is guaranteed
    to be no worse than the average input quality but can improve with small
    probability. If all inputs are same category, the crafted item preserves
    that category where possible.
    """

    MODES = ["probabilistic", "deterministic", "fusion", "upgrade"]
    # Human-friendly labels for modes (Russian)
    MODE_LABELS = {
        "probabilistic": "Вероятностный",
        "deterministic": "Детерминированный",
        "fusion": "Слияние",
        "upgrade": "Апгрейд",
    }

    def _build_display_rows(self) -> List[Tuple[str, str, int, int, float | None]]:
        """Return rows similar to InventoryScene: (item_id, name, base_price, adj_price, qual)"""
        owned = self.state.inventory.get_items()
        rows: List[Tuple[str, str, int, int, float | None]] = []
        # sort by price asc for stable listing
        ordered = sorted(owned, key=lambda ic: ic[0].price)
        for it, cnt in ordered:
            qlist = self.state.inventory.get_item_qualities(it.id)
            if qlist:
                for q in qlist:
                    mult = price_multiplier(q)
                    adj = int(round(it.price * mult))
                    rows.append((it.id, it.name, it.price, adj, float(q)))
            else:
                rows.append((it.id, it.name, it.price, it.price, None))
        return rows

    def _print_rows(self, rows: List[Tuple[str, str, int, int, float | None]]) -> None:
        if not rows:
            self.console.write_line("У вас нет предметов в инвентаре.")
            return
        # print enumerated rows — show only name, скорректированная цена (adj) и quality
        for i, (_iid, name, _base, adj, qual) in enumerate(rows, start=1):
            qtxt = f"{qual:.6f}" if qual is not None else "-"
            self.console.write_line(f"{i:3d}. {name}    ценность={adj}    качество={qtxt}")

    def _show_modes_guide(self) -> None:
        """Show a short, user-friendly guide describing each crafting mode."""
        self.console.clear()
        self.console.write_line("Гайд по режимам крафта:\n")
        self.console.write_line("1) Вероятностный (Вероятностный):\n  - Вы выбираете 2–8 предметов и уровень шанса (50/35/25/10).\n  - При успехе создаётся новый предмет; при провале входные предметы сгорают и предмет не создаётся.\n  - Чем ниже шанс, тем выше потенциальная ценность результата.")
        self.console.write_line("")
        self.console.write_line("2) Детерминированный (Детерминированный):\n  - Объединяет предметы предсказуемо, результат гарантирован.\n  - Используйте, когда хотите предсказуемый исход и не рисковать потерей входов.")
        self.console.write_line("")
        self.console.write_line("3) Слияние (Слияние):\n  - Комбинирует несколько предметов, качество результирующего — усреднение/специальная логика.\n  - Результат гарантирован; входы сгорают и получаете новый предмет.")
        self.console.write_line("")
        self.console.write_line("4) Апгрейд (Апгрейд):\n  - Попытка повысить качество одного предмета.\n  - При успехе вы получите новый предмет с новым качеством; при провале входной предмет сгорает.")
        #self.console.write_line("")
        #self.console.write_line("Нажмите Enter, чтобы вернуться к выбору режима.")
        self.console.wait_for_key()

    def run(self) -> Optional[str]:
        while True:
            self.console.clear()
            self.console.write_line("=== Крафт предметов ===")
            self.console.write_line("Выберите режим крафта:")
            for i, m in enumerate(self.MODES, start=1):
                label = self.MODE_LABELS.get(m, m)
                self.console.write_line(f"  {i}. {label}")
            self.console.write_line("  g. Гайд по режимам")
            self.console.write_line("  q. Назад")
            choice = self.console.read_input("Режим: ").strip().lower()
            if choice in ("q", "b"):
                return "menu"
            if choice == "g":
                # show a short user-friendly guide explaining each mode
                self._show_modes_guide()
                continue
            if not choice.isdigit() or int(choice) < 1 or int(choice) > len(self.MODES):
                self.console.write_line("Неверный выбор. Нажмите Enter и попробуйте снова.")
                self.console.wait_for_key()
                continue

            mode = self.MODES[int(choice) - 1]

            # Show inventory rows and ask user to select indices
            rows = self._build_display_rows()
            self.console.clear()
            self.console.write_line(f"Режим: {mode}")
            self.console.write_line("")
            self.console.write_line("Выберите предметы для крафта (номера через пробел).")
            if mode == "upgrade":
                self.console.write_line("(для апгрейда выберите ровно 1 предмет)")
            else:
                self.console.write_line("(минимум 2, максимум 8 предметов)")
            self.console.write_line("")
            self._print_rows(rows)
            if not rows:
                self.console.wait_for_key()
                return "menu"

            sel_raw = self.console.read_input("Выбор: ").strip()
            if not sel_raw:
                continue
            try:
                indices = [int(x) - 1 for x in sel_raw.split()]
            except Exception:
                self.console.write_line("Неверный ввод индексов.")
                self.console.wait_for_key()
                continue

            # validate indices
            if any(i < 0 or i >= len(rows) for i in indices):
                self.console.write_line("Один из индексов вне диапазона.")
                self.console.wait_for_key()
                continue

            if mode == "upgrade" and len(indices) != 1:
                self.console.write_line("Для апгрейда выберите ровно один предмет.")
                self.console.wait_for_key()
                continue

            if mode != "upgrade" and not (2 <= len(indices) <= 8):
                self.console.write_line("Выберите от 2 до 8 предметов для этого режима.")
                self.console.wait_for_key()
                continue

            # Build selections (item_id, quality)
            selections: List[Tuple[str, float]] = []
            for i in indices:
                iid, name, base, adj, qual = rows[i]
                if qual is None:
                    # For items without per-instance quality we treat quality as 0.0
                    q = 0.0
                else:
                    q = float(qual)
                selections.append((iid, q))

            # Choose tier for probabilistic/upgrade; deterministic/fusion ignore tier
            tier = 50
            if mode in ("probabilistic", "upgrade"):
                self.console.write_line("")
                self.console.write_line("Выберите шанс/уровень (введите число):")
                self.console.write_line("  50 - 50% (низкий выигрыш)")
                self.console.write_line("  35 - 35% (средний выигрыш)")
                self.console.write_line("  25 - 25% (больший выигрыш)")
                self.console.write_line("  10 - 10% (очень большой выигрыш)")
                t_raw = self.console.read_input("Шанс (50/35/25/10): ").strip()
                try:
                    t_val = int(t_raw)
                    if t_val in TIERS:
                        tier = t_val
                    else:
                        self.console.write_line("Неверный уровень, выбран 50% по умолчанию.")
                        tier = 50
                except Exception:
                    self.console.write_line("Неверный ввод, выбран 50% по умолчанию.")
                    tier = 50

            # Preview: compute adjusted sum and cost
            from case_simulator.utils.crafting import compute_adjusted_sum

            adjusted_sum = compute_adjusted_sum(selections)
            # Цена крафта: 0.2% от суммарной скорректированной стоимости (пользовательская настройка)
            cost = max(1, int(round(adjusted_sum * 0.002)))
            self.console.write_line("")
            self.console.write_line(f"Суммарная скорректированная стоимость входов: {adjusted_sum:.2f}")
            self.console.write_line(f"Цена крафта (0.2%): {cost} монет")
            self.console.write_line(f"Ваш баланс: {self.state.balance} монет")

            # confirm
            conf = self.console.read_input("Подтвердить крафт? (y/n): ").strip().lower()
            if conf != "y":
                self.console.write_line("Отменено.")
                self.console.wait_for_key()
                continue

            # Check balance
            if not self.state.try_deduct(cost):
                self.console.write_line("Недостаточно средств для крафта.")
                self.console.wait_for_key()
                continue

            # Burn selected items (remove per-instance by quality). We remove in the
            # order selected; remove_item_by_quality picks closest quality if exact
            # match not found.
            for iid, q in selections:
                ok = self.state.inventory.remove_item_by_quality(iid, float(q))
                if not ok:
                    # This should not happen but handle gracefully: refund and abort
                    self.state.add_balance(cost)
                    self.console.write_line("Не удалось удалить выбранные предметы. Откат операции.")
                    self.console.wait_for_key()
                    return "menu"

            # Perform craft logic
            res = craft_items(self.state, selections, mode, tier)

            out = res.get("output")
            success = res.get("success")

            if out is None:
                self.console.write_line("Крафт завершён, но не удалось сгенерировать результат.")
                self.console.wait_for_key()
                return "menu"

            # We'll only add the created item to inventory if the craft was successful.
            out_id = out["id"]

            # Present result — do not show ordinary id or base price here; show name and quality
            # compute adjusted price for the created output (price * price_multiplier(quality))
            try:
                mult_out = price_multiplier(float(out.get("quality", 0.0)))
                adj_out_price = int(round(out.get("price", 0) * mult_out))
            except Exception:
                mult_out = 1.0
                adj_out_price = int(out.get("price", 0))

            if success:
                # Add output to inventory (register transient template if needed)
                if out_id in presets.ITEMS_BY_ID:
                    tmpl = presets.ITEMS_BY_ID[out_id]
                    self.state.inventory.add_item(tmpl, qty=1, quality=float(out["quality"]))
                else:
                    tmpl = Item(id=out_id, name=out["name"], price=int(out.get("price", 0)), category=out.get("category", "weapon"), rare=0, quality=0.0)
                    self.state.inventory.register_item(tmpl)
                    self.state.inventory.add_item(tmpl, qty=1, quality=float(out["quality"]))

                self.console.write_line("")
                self.console.write_line("Крафт успешен! Вы получили:")
                self.console.write_line(f"  {out['name']}  качество={out['quality']:.6f}")
                self.console.write_line(f"  Скорректированная цена нового предмета: {adj_out_price} (множитель={mult_out:.3f})")
            else:
                # On failure input items are burned and no item is added to inventory.
                self.console.write_line("")
                self.console.write_line("Крафт завершён (провал). Входные предметы сожжены; предмет не добавлен в инвентарь.")
                # Optionally show what would have been generated (informational)
                self.console.write_line(f"  Сгенерированный (не добавлен): {out['name']}  качество={out['quality']:.6f}")
                self.console.write_line(f"  Скорректированная цена (инфо): {adj_out_price} (множитель={mult_out:.3f})")

            self.console.write_line("")
            self.console.write_line(f"Стоимость операции: {res.get('cost')} (списано). Среднее качество входов: {res.get('avg_q'):.6f}")
            self.console.write_line("Нажмите Enter для возврата в меню крафта.")
            self.console.wait_for_key()
            return "menu"
