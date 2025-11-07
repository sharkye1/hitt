from __future__ import annotations

import random
from typing import Tuple


def gen_quality() -> float:
    """Generate a quality value in [0.0, 1.0) rounded to 6 decimals.

    This reproduces the same behaviour that was previously inside the
    CaseOpeningScene._gen_quality: a beta-distributed base with a small
    chance to produce boosted ultra-rare values in specific bands.

    Генерирует значение качества в диапазоне [0.0, 1.0), округленное до 6 десятичных знаков.

    Это воспроизводит то же поведение, что и раньше внутри CaseOpeningScene._gen_quality: 
    базовое распределение бета с небольшой
    шанс получить повышенные ультра-редкие значения в определенных диапазонах.
    """
    # Base distribution: beta with mean ~0.85 (alpha/(alpha+beta) = 17/(17+3) = 0.85)

    # Базовое распределение: бета с средним ~0.85 (альфа/(альфа+бета) = 17/(17+3) = 0.85)
    q = random.betavariate(17.0, 3.0)

    # редкая вероятность получить ультра-высокое качество из определенных диапазонов
    r = random.random()
    if r < 0.005:  # 0.5% chance for boosted rare quality
        s = random.random()
        if s < 0.6:
            # 0.9900 .. 0.9950
            q = 0.99 + random.random() * (0.0050)
        elif s < 0.95:
            # 0.9951 .. 0.9989
            q = 0.9951 + random.random() * (0.0038)
        else:
            # 0.9990 .. 0.9999
            q = 0.9990 + random.random() * (0.0009)

    # Ensure strictly < 1.0 and round to 6 decimals
    # Убедитесь, что значение строго меньше 1.0 и округлено до 6 десятичных знаков
    q = min(q, 0.999999)
    q = round(q, 6)
    if q >= 1.0:
        q = 0.999999
    return float(q)


# Threshold helpers used by the report/simulation to classify "rare" bands
# Пороговые помощники, используемые отчетом/симуляцией для классификации "редких" диапазонов
def is_ge_0_99(q: float) -> bool:
    return q >= 0.99


def is_ge_0_9951(q: float) -> bool:
    return q >= 0.9951


def is_ge_0_9990(q: float) -> bool:
    return q >= 0.9990
