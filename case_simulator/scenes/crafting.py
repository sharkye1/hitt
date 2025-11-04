from __future__ import annotations

from typing import Optional

from case_simulator.scenes.base import Scene


class CraftingScene(Scene):
    """Stub scene for future crafting mechanics."""

    def run(self) -> Optional[str]:
        self.console.clear()
        self.console.write_line("=== Крафт предметов ===")
        self.console.write_line("Здесь появится логика крафта.")
        self.console.write_line("Добавьте рецепты, улучшения и другие правила.")
        self.console.write_empty_line()
        self.console.wait_for_key("Нажмите Enter или Esc для возврата в меню...")
        return "menu"
