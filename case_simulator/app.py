from __future__ import annotations

from typing import Dict, Optional

from case_simulator.scenes.base import Scene
from case_simulator.scenes.case_opening import CaseOpeningScene
from case_simulator.scenes.crafting import CraftingScene
from case_simulator.scenes.main_menu import MainMenuScene
from case_simulator.scenes.shop import ShopScene
from case_simulator.utils.console import Console
from case_simulator.state import GameState
from case_simulator.save_manager import SaveManager


class CaseSimulatorApp:
    """Класс основного приложения симулятора кейсов."""

    def __init__(self) -> None:
        self.console = Console()
        self.save_manager = SaveManager()
        
        # Загружаем состояние из сохранения или создаем новое
        self.state = self.save_manager.load()
        
        self.scenes: Dict[str, Scene] = {
            "menu": MainMenuScene(self.console, self.state),
            "case_opening": CaseOpeningScene(self.console, self.state),
            "crafting": CraftingScene(self.console, self.state),
            "shop": ShopScene(self.console, self.state),
        }

    def run(self) -> None:
        """Запустить основной цикл до тех пор, пока сцена не попросит выйти."""
        next_scene_name: Optional[str] = "menu"

        while next_scene_name:
            scene = self.scenes[next_scene_name]
            next_scene_name = scene.run()
            
            # Сохраняем состояние после каждой сцены
            self.save_manager.save(self.state)

        self.console.clear()
        self.console.write_line("Спасибо за игру! До встречи.")
        
        # Финальное сохранение перед выходом
        self.save_manager.save(self.state)
