from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Item:
    """Базовый предмет (оружие, скин и т.п.).

    id: строковый идентификатор шаблона предмета (используется в каталоге)
    name: отображаемое имя
    price: стоимость предмета в игровой валюте
    category: произвольная категория (например: weapon, knife, misc)
    """

    id: str
    name: str
    price: int
    category: str = "misc"
    rare: int = 0
