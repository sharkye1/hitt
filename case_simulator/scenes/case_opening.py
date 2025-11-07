from __future__ import annotations

import random
import time
from typing import Optional, List, Tuple

from case_simulator.scenes.base import Scene
from case_simulator.models.case import Case
from case_simulator.models.item import Item
from case_simulator.data import presets
from case_simulator.utils.pricing import price_multiplier
from case_simulator.utils.quality import gen_quality
import sys
import math


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
            self.console.write_line("Q - Назад")
            self.console.write_empty_line()

            # Try single-key selection for convenience
            try:
                choice = self.console.read_key("Выберите кейс для открытия (Q - назад): ").strip()
            except Exception:
                choice = self.console.read_input("Выберите кейс для открытия (Q - назад): ").strip()
            # Поддерживаем как 'q'/'Q', так и старый вариант '0' для совместимости
            if choice.lower() == "q" or choice == "0":
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
        total_steps = min(len(items) * 2 + win_index, 25)

        # Анимация: показываем сменяющиеся элементы в одной строке.
        # Требование: между 1-м и 2-м показом очень мало (~0.05s),
        # между 2-м и 3-м чуть больше, а финальные паузы — около 0.6–0.8s.
        start_delay = 0.05
        final_delay = 0.6 + random.random() * 0.2  # 0.6 .. 0.8

        # Подготовим паддинг, чтобы очистить предыдущую надпись при переписывании
        display_texts = [f"→ {it.name}" for it in items]
        max_len = max(len(t) for t in display_texts)

        for step in range(total_steps):
            current = items[step % len(items)]
            text = f"→ {current.name}"
            padded = text + " " * (max_len - len(text))

            # t in [0,1) progress through animation; use eased (quadratic) curve
            # t принадлежит [0,1) прогресс через анимацию; используем квадратичную кривую
            t = step / max(1, total_steps - 1)
            # возрастающая квадратичная кривая для замедления в конце
            delay = start_delay + (final_delay - start_delay) * (t * t)

            
            try:
                sys.stdout.write("\r" + padded)
                sys.stdout.flush()
            except Exception:
                # fallback to printing new line if direct stdout write fails
                self.console.write_line(padded)

            time.sleep(delay)

        # окончание анимации — переведём курсор на новую строку
        try:
            sys.stdout.write("\n")
            sys.stdout.flush()
        except Exception:
            self.console.write_empty_line()

        winner = items[win_index]

        # Генерируем качество предмета (6 знаков после запятой, в диапазоне [0.0, 1.0))
        q = self._gen_quality()

        # Рассчитываем множитель цены по качеству и итоговую цену предмета
        multiplier = price_multiplier(q)
        adj_price = max(1, int(round(winner.price * multiplier)))

        self.console.write_line(f"Выпало: {winner.name} (качество {q:.6f}, базовая цена {winner.price}, скорр. цена {adj_price})")

        # Предложение: оставить или продать за 88% от скорректированной цены
        sell_price = int(adj_price * 0.88)
        self.console.write_line(f"1. Оставить (в инвентарь)")
        self.console.write_line(f"2. Продать за {sell_price}")
        self.console.write_empty_line()

        while True:
            # allow single-key press (no Enter) for faster UX
            try:
                action = self.console.read_key("Ваш выбор: ").strip()
            except Exception:
                action = self.console.read_input("Ваш выбор: ").strip()
            if action == "1":
                # Сохраняем предмет в инвентарь как экземпляр с конкретным quality
                # Создаём новый объект Item-экземпляр, но не перезаписываем каталог
                inst = Item(
                    id=winner.id,
                    name=winner.name,
                    price=winner.price,
                    category=winner.category,
                    rare=winner.rare,
                    quality=q,
                )
                self.state.inventory.add_item(inst, 1, quality=q)
                self.console.write_line("Предмет добавлен в инвентарь.")
                break
            if action == "2":
                self.state.add_balance(sell_price)
                self.console.write_line(f"Продано. Баланс: {self.state.balance}")
                break
            self.console.write_line("Введите 1 или 2.")

            self.console.write_empty_line()
            self.console.wait_for_key("Нажмите Enter или Esc для возврата к списку кейсов...")

    # --- quality & pricing helpers ---
    def _gen_quality(self) -> float:
        # Delegate to shared generator for consistency with simulations
        return gen_quality()

    def _price_multiplier(self, q: float) -> float:
        """Сопоставление качества q с множителем цены согласно настроенным уровням.
        q: float в диапазоне [0.0, 1.0)        
        """
        # Safety clamp
        q = max(0.0, min(q, 0.999999))

        # Below 0.5: linear from 0.4 -> 0.65 at 0.5
        if q < 0.5:
            return 0.4 + (0.65 - 0.4) * (q / 0.5)

        # 0.5 .. 0.75: linear 0.65 -> 0.75
        if q < 0.75:
            return 0.65 + (0.75 - 0.65) * ((q - 0.5) / 0.25)

        # 0.75 .. 0.9: linear 0.75 -> 1.0
        if q < 0.9:
            return 0.75 + (1.0 - 0.75) * ((q - 0.75) / 0.15)

        # Anchors for >0.9 progression
        # Привязки для прогрессии >0.9
        anchors = [
            (0.9, 1.0),
            (0.91, 1.05),
            (0.93, 1.30),
            (0.95, 1.70),
            (0.99, 3.00),
            (0.9950, 5.00),
        ]

        # between 0.9 and 0.995: linear interpolate between anchors
        # между 0.9 и 0.995: линейная интерполяция между привязками
        for i in range(len(anchors) - 1):   
            x0, m0 = anchors[i]
            x1, m1 = anchors[i + 1]
            if x0 <= q < x1:
                t = (q - x0) / (x1 - x0)
                return m0 + (m1 - m0) * t

        # 0.9950 < q <= 0.9989 -> fixed 8.0 (800%) according to spec
        # 0.9950 < q <= 0.9989 -> фиксированное значение 8.0 (800%) согласно спецификации
        if q <= 0.9989:
            if q > 0.9950:
                return 8.0

        # q >= 0.9990 -> progressive per-0.0001 increments starting at 10.0
        # q >= 0.9990 -> прогрессивные приращения по 0.0001, начиная с 10.0
        if q >= 0.9990:
            # number of steps of 0.0001 above 0.9990
            steps = (q - 0.9990) / 0.0001
            return 10.0 + steps

        # fallback: if q in small gap between 0.9989 and 0.9990, return 8.0
        # запасной вариант: если q в небольшом промежутке между 0.9989 и 0.9990, вернуть 8.0
        return 8.0
    