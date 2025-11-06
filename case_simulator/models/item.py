from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Item:
    """Базовый предмет (оружие, скин и т.п.).

    id: строковый идентификатор шаблона предмета (используется в каталоге)
    name: отображаемое имя
    price: стоимость предмета в игровой валюте
    category: произвольная категория (например: weapon, knife, misc)
    rare: уровень редкости (чем выше, тем реже предмет встречается в кейсах)
    quality: качество предмета (число с плавающей точкой от 0.0 до 1.0)
    """

    id: str
    name: str
    price: int
    category: str = "misc"
    rare: int = 0
    quality: float = 0.0 

    def __post_init__(self) -> None:
        # Качество должно быть float между 0.0 и 1.0 включительно.
        # Поскольку dataclass заморожен, мы вызываем ошибку, когда предоставлено недопустимое значение.
        # Quality validation 
        # Ensure quality is a float between 0.0 and 1.0 inclusive.
        try:
            q = float(self.quality)
        except Exception:
            raise TypeError(f"качество должно быть float между 0.0 и 1.0, получено {self.quality!r}"
                            f"quality must be a float between 0.0 and 1.0, got {self.quality!r}")

        if not (0.0 <= q <= 1.0):
            raise ValueError(f"качество должно быть между 0.0 и 1.0 (включительно), получено {q}"
                             f"quality must be between 0.0 and 1.0 (inclusive), got {q}")
