from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from case_simulator.models.item import Item


@dataclass(frozen=True)
class Case:
    """Базовый кейс.

    id: строковый идентификатор шаблона кейса (используется в каталоге)
    name: отображаемое имя кейса
    price: стоимость открытия кейса (или его рыночная цена)
    items: фиксированный набор потенциальных предметов из кейса
    """

    id: str
    name: str
    price: int
    items: Tuple[Item, ...]
