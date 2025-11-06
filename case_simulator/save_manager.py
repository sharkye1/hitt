from __future__ import annotations

import base64
import json
from pathlib import Path
from typing import Any, Dict

from case_simulator.state import GameState
from case_simulator.models.inventory import Inventory
from case_simulator.data import presets


class SaveManager:
    """Управление сохранением/загрузкой состояния игры с базовым шифрованием."""

    _SAVE_FILE = "savegame.dat"
    _XOR_KEY = b"case_simulator_secret_key_2025"

    def __init__(self, save_dir: Path | None = None) -> None:
        self.save_dir = save_dir or Path.cwd()
        self.save_path = self.save_dir / self._SAVE_FILE

    def save(self, state: GameState) -> None:
        """Сохранить состояние игры в зашифрованный файл."""
        # Сериализуем данные
        data: Dict[str, Any] = {
            "balance": state.balance,
            "item_counts": state.inventory.item_counts,
            "case_counts": state.inventory.case_counts,
            # Явный список пресетов/кейсов, которые уже были выданы игроку
            # (чтобы при появлении новых пресетов в репозитории не выдавать
            # их повторно одному и тому же игроку).
            "granted_presets": getattr(state, "granted_presets", []),
            # Per-instance qualities for items (id -> list of floats)
            "item_qualities": getattr(state.inventory, "item_qualities", {}),
        }
        json_str = json.dumps(data, ensure_ascii=False, indent=2)
        
        # Шифруем XOR + base64
        encrypted = self._encrypt(json_str.encode("utf-8"))
        
        # Записываем в файл
        self.save_path.write_bytes(encrypted)

    def load(self) -> GameState:
        """Загрузить состояние из файла или создать новое."""
        if not self.save_path.exists():
            # Первый запуск — создаем стартовое состояние
            return self._create_fresh_state()

        try:
            # Читаем и расшифровываем
            encrypted = self.save_path.read_bytes()
            decrypted = self._decrypt(encrypted)
            data = json.loads(decrypted.decode("utf-8"))

            # Восстанавливаем каталоги из presets (регистрируем все кейсы/предметы)
            inventory = presets.create_sample_inventory()

            # Накатываем сохраненные количества (если игрок когда-то что-то менял)
            inventory.item_counts = data.get("item_counts", {})
            inventory.case_counts = data.get("case_counts", {})
            inventory.item_qualities = data.get("item_qualities", {})

            # Сохранившиеся пресеты, которые уже выдавали игроку
            granted: list[str] = data.get("granted_presets", [])

            # Определим пресеты, добавленные в текущей версии `presets.py`, но
            # которых нет в сохранённом case_counts — это кандидаты на разовую
            # выдачу новому или "не знавшему" игроку.
            preset_ids = set(presets.FREE_PRESET_CASES.keys())
            saved_case_ids = set(inventory.case_counts.keys())

            newly_granted: list[str] = []
            for pid in sorted(preset_ids):
                # если в сохранении нет ключа — считаем пресет "новым" для
                # этого игрока и выдаём его (но только если не было отмечено
                # как выданный ранее через granted_presets)
                if pid not in saved_case_ids and pid not in granted:
                    qty = presets.FREE_PRESET_CASES.get(pid, 0)
                    case_obj = inventory.case_catalog.get(pid)
                    if case_obj and qty > 0:
                        inventory.add_case(case_obj, qty=qty)
                        newly_granted.append(pid)

            # Обновляем список granted_presets и при необходимости сохраняем
            # сразу, чтобы при следующем запуске не выдать повторно.
            granted.extend(newly_granted)

            state = GameState(
                inventory=inventory,
                balance=data.get("balance", 0),
                granted_presets=granted,
            )

            if newly_granted:
                # Сохраняем обновлённый файл, включающий granted_presets
                self.save(state)

            return state
        except Exception as e:
            # Если файл поврежден, создаем новое состояние
            print(f"Ошибка загрузки сохранения: {e}. Создано новое состояние.")
            return self._create_fresh_state()

    def _create_fresh_state(self) -> GameState:
        """Создать стартовое состояние с примерами."""
        # Создаём каталог предметов/кейсов, но не выдаём никаких предметов по умолчанию.
        # Это позволяет иметь пустой инвентарь, но при этом регистрация всех
        # типов предметов/кейсов доступна для кода (например, для магазина/инвентаря).
        inventory = presets.create_sample_inventory()

        # При первом запуске выдаём игроку несколько стартовых (дешёвых)
        # кейсов, чтобы у него было с чем играть. Сопоставление
        # FREE_PRESET_CASES описывает, какие кейсы и в каких
        # количествах должны быть выданы один раз при появлении пресета.
        granted: list[str] = []
        for pid, qty in presets.FREE_PRESET_CASES.items():
            case_obj = inventory.case_catalog.get(pid)
            if case_obj and qty > 0:
                inventory.add_case(case_obj, qty=qty)
                granted.append(pid)

        # Начальный баланс — 500 (как запросил пользователь)
        state = GameState(inventory=inventory, balance=500, granted_presets=granted)

        # Сохраняем сразу, чтобы при следующем запуске этот начальный файл
        # считался существующим и не перегенерировал стартовые пресеты.
        self.save(state)
        return state

    def _encrypt(self, data: bytes) -> bytes:
        """XOR-шифрование + base64."""
        xored = self._xor_bytes(data, self._XOR_KEY)
        return base64.b64encode(xored)

    def _decrypt(self, data: bytes) -> bytes:
        """Обратное преобразование: base64 + XOR."""
        decoded = base64.b64decode(data)
        return self._xor_bytes(decoded, self._XOR_KEY)

    @staticmethod
    def _xor_bytes(data: bytes, key: bytes) -> bytes:
        """XOR каждого байта данных с циклическим ключом."""
        return bytes(b ^ key[i % len(key)] for i, b in enumerate(data))
