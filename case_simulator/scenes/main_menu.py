from __future__ import annotations

from typing import Optional

from case_simulator.scenes.base import Scene


class MainMenuScene(Scene):
    """Primary navigation scene."""

    def run(self) -> Optional[str]:
        while True:
            self.console.clear()
            self.console.write_line("=== Симулятор кейсов ===")
            self.console.write_line(f"Баланс: {self.state.balance}")
            self.console.write_line("1. Открытие кейсов")
            self.console.write_line("2. Крафт предметов")
            self.console.write_line("3. Магазин")
            self.console.write_line("0. Выход")
            self.console.write_empty_line()

            choice = self.console.read_input("Выберите режим: ")

            if choice == "1":
                return "case_opening"
            if choice == "2":
                return "crafting"
            if choice == "3":
                return "shop"
            if choice == "0":
                return None

            self.console.write_line("Неизвестный вариант. Попробуйте снова.")
            self.console.wait_for_key("Нажмите Enter или Esc для продолжения...")
