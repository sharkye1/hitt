from __future__ import annotations

import random
import time
from typing import Optional, List, Tuple

from case_simulator.scenes.base import Scene
from case_simulator.models.case import Case
from case_simulator.models.item import Item
from case_simulator.data import presets


class CaseOpeningScene(Scene):
    """Сцена открытия кейсов."""

    def run(self) -> Optional[str]:
        while True:
            self.console.clear()
            self.console.write_line("=== Открытие кейсов ===")
            self.console.write_line(f"Баланс: {self.state.balance}")
            self.console.write_empty_line()

            cases = self.state.inventory.get_cases()
            if not cases:
                self.console.write_line("В инвентаре нет доступных кейсов.")
                self.console.write_empty_line()
                self.console.wait_for_key("Нажмите Enter или Esc для возврата в меню...")
                return "menu"

            # Список кейсов
            for idx, (case, count) in enumerate(cases, start=1):
                self.console.write_line(f"{idx}. {case.name} (x{count}) — цена {case.price}")
            self.console.write_line("0. Назад")
            self.console.write_empty_line()

            choice = self.console.read_input("Выберите кейс для открытия: ")
            if choice == "0":
                return "menu"
            if not choice.isdigit():
                self.console.write_line("Введите номер из списка.")
                self.console.wait_for_key("Нажмите Enter или Esc для продолжения...")
                continue

            idx = int(choice) - 1
            if idx < 0 or idx >= len(cases):
                self.console.write_line("Нет такого варианта.")
                self.console.wait_for_key("Нажмите Enter или Esc для продолжения...")
                continue

            case, count = cases[idx]
            if count <= 0:
                self.console.write_line("Кейс закончился.")
                self.console.wait_for_key("Нажмите Enter или Esc для продолжения...")
                continue

            # Открыть выбранный кейс
            self._open_case(case)
            # После открытия вернемся к списку для возможности открыть еще

    # --- Внутренняя логика ---
    def _open_case(self, case: Case) -> None:
        # Списать один кейс
        removed = self.state.inventory.remove_case(case, qty=1)
        if not removed:
            self.console.write_line("Не удалось открыть кейс: нет в инвентаре.")
            self.console.wait_for_key("Нажмите Enter или Esc для продолжения...")
            return

        self.console.clear()
        self.console.write_line(f"Открываем кейс: {case.name}")
        self.console.write_empty_line()
        self.console.write_line("Рулетка...")

        items: List[Item] = list(case.items)
        if not items:
            self.console.write_line("Кейс пуст :(")
            self.console.wait_for_key("Нажмите Enter или Esc для продолжения...")
            return

        # Выберем приз заранее и построим анимацию с замедлением
        # Взвешенный выбор: используем параметры из `presets.py` чтобы
        # сделать редкие предметы ещё реже, но при этом не допустить нулевых шансов.
        # Формула: raw = 1 / (rare ** power)  (rare>0), raw=1 для rare<=0
        # weight = max(DROP_MIN_WEIGHT, raw * DROP_WEIGHT_MULTIPLIER)
        weights: List[float] = []
        power = getattr(presets, "DROP_RARE_POWER", 1.0)
        min_w = getattr(presets, "DROP_MIN_WEIGHT", 1e-6)
        mult = getattr(presets, "DROP_WEIGHT_MULTIPLIER", 1.0)

        for it in items:
            try:
                r = float(getattr(it, "rare", 0) or 0)
            except Exception:
                r = 0.0
            if r <= 0:
                raw = 1.0
            else:
                raw = 1.0 / (r ** float(power))
            w = max(float(min_w), float(raw) * float(mult))
            weights.append(w)

        # random.choices поддерживает взвешенный выбор (Python 3.6+).
        try:
            winner = random.choices(items, weights=weights, k=1)[0]
            win_index = items.index(winner)
        except Exception:
            # Фоллбек на равновероятный выбор
            win_index = random.randrange(len(items))
        total_steps = len(items) * 2 + win_index  # пару полных кругов + финиш на призе

        # Параметры замедления
        delay = 0.5 # начальная задержка
        delay_growth = 1.5  # множитель замедления

        for step in range(total_steps):
            current = items[step % len(items)]
            self.console.write_line(f"→ {current.name}")
            time.sleep(delay)
            delay = min(delay * delay_growth, 0.45)

        winner = items[win_index]
        self.console.write_empty_line()
        self.console.write_line(f"Выпало: {winner.name} (стоимость {winner.price})")

        # Предложение: оставить или продать за 80%
        sell_price = int(winner.price * 0.8)
        self.console.write_line(f"1. Оставить (в инвентарь)")
        self.console.write_line(f"2. Продать за {sell_price}")
        self.console.write_empty_line()

        while True:
            action = self.console.read_input("Ваш выбор: ")
            if action == "1":
                self.state.inventory.add_item(winner, 1)
                self.console.write_line("Предмет добавлен в инвентарь.")
                break
            if action == "2":
                self.state.add_balance(sell_price)
                self.console.write_line(f"Продано. Баланс: {self.state.balance}")
                break
            self.console.write_line("Введите 1 или 2.")

        self.console.write_empty_line()
        self.console.wait_for_key("Нажмите Enter или Esc для возврата к списку кейсов...")
    