from __future__ import annotations

from case_simulator.models.item import Item
from case_simulator.models.case import Case
from case_simulator.models.inventory import Inventory


# Примеры предметов — расширенные: несколько пистолетов, винтовок, AWP и редкий нож
# Пистолеты (более частые)
PISTOL_MK1 = Item(id="pistol_mk1", name="Pistol Mk1", price=100, category="pistol", rare=1)
PISTOL_MK2 = Item(id="pistol_mk2", name="Pistol Mk2", price=140, category="pistol", rare=1)
PISTOL_MK3 = Item(id="pistol_mk3", name="Pistol Mk3", price=180, category="pistol", rare=2)

# Винтовки (реже и дороже)
RIFLE_BASIC = Item(id="rifle_basic", name="Rifle Basic", price=450, category="rifle", rare=3)
RIFLE_PRO = Item(id="rifle_pro", name="Rifle Pro", price=650, category="rifle", rare=4)

# AWP — очень редкий и дорогой снайперский ски
AWP_LEGEND = Item(id="awp_legend", name="AWP Legend", price=3000, category="sniper", rare=8)

# Ножи: один дешёвый и один легендарный (для knife-case)
KNIFE_RUSTY = Item(id="knife_rusty", name="Rusty Knife", price=250, category="knife", rare=2)
KNIFE_LEGEND = Item(id="knife_legend", name="Legendary Knife", price=8000, category="knife", rare=10)


# Новые кейсы по категориям: пистолеты, винтовки, AWP и нож-кейс
PISTOL_CASE = Case(
    id="pistol_case",
    name="Pistol Case",
    price=120,
    items=(PISTOL_MK1, PISTOL_MK2, PISTOL_MK3),
)

RIFLE_CASE = Case(
    id="rifle_case",
    name="Rifle Case",
    price=400,
    items=(RIFLE_BASIC, RIFLE_PRO),
)

AWP_CASE = Case(
    id="awp_case",
    name="AWP Case",
    price=2500,
    items=(AWP_LEGEND, RIFLE_PRO),
)

# Нож-кейс — очень дорогой и почти неокупаемый по задумке
KNIFE_CASE = Case(
    id="knife_case",
    name="Knife Case",
    price=10000,
    items=(KNIFE_LEGEND, KNIFE_RUSTY),
)


# Коллекции предметов и кейсов — удобно итерации и быстрый доступ по id
ITEMS = (
    PISTOL_MK1,
    PISTOL_MK2,
    PISTOL_MK3,
    RIFLE_BASIC,
    RIFLE_PRO,
    AWP_LEGEND,
    KNIFE_RUSTY,
    KNIFE_LEGEND,
)
CASES = (PISTOL_CASE, RIFLE_CASE, AWP_CASE, KNIFE_CASE)

# Быстрый доступ по id
ITEMS_BY_ID = {it.id: it for it in ITEMS}
CASES_BY_ID = {c.id: c for c in CASES}


def create_sample_inventory() -> Inventory:
    inv = Inventory()

    # Зарегистрируем шаблоны (на будущее, если добавятся новые дропы)
    # используем коллекции выше, чтобы не перечислять вручную
    for item in ITEMS:
        inv.register_item(item)
    for case in CASES:
        inv.register_case(case)
    
    # NOTE: Не добавляем стартовые количества кейсов здесь. Стартовые/подарочные
    # контролируются FREE_PRESET_CASES (ниже) и предоставляются
    # SaveManager при создании нового сохранения или при появлении новых пресетов.

    # Мы храним пару стартовых предметов в каталоге, но не мутируем
    # постоянные количества здесь (так что предоставление может быть выполнено в одном месте).

    return inv


# Сопоставление case_id -> qty, которое должно быть выдано один раз каждому игроку, когда
# кейс будет представлен в `presets.py`. Добавляйте новые записи здесь, когда добавляете
# новые бесплатные/промо-кейсы в репозиторий. SaveManager гарантирует, что каждый
# id из этого сопоставления будет добавлен в инвентарь игрока не более одного раза.
FREE_PRESET_CASES: dict[str, int] = {
    # бесплатные пресеты: даём новичкам несколько пистолетных кейсов и один ружейный
    "pistol_case": 2,
    "rifle_case": 1,
}


# Магазин — набор товаров, которые можно купить.
# Формат:
# SHOP_STOCK = {
#   "object_id": {"type": "case"|"item", "price": <int>, "stock": <int|None>},
# }
# - price: цена продажи в магазине (если не указана, используется price объекта из каталога)
# - stock: None означает неограниченный запас; целое число — ограниченный запас.
#
# Примечание: эта структура хранится как константа в коде; уменьшение stock при
# покупках происходит в памяти во время выполнения процесса. Если нужно
# персистировать остатки магазина, потребуется сохранить их в файле/БД.
SHOP_STOCK: dict[str, dict] = {
    # Основные кейсы в магазине
    "pistol_case": {"type": "case", "price": 120, "stock": None},
    "rifle_case": {"type": "case", "price": 400, "stock": 5},
    "awp_case": {"type": "case", "price": 2500, "stock": 1},
    # Нож-кейс очень дорогой и редкий
    "knife_case": {"type": "case", "price": 10000, "stock": 1},

    # некоторые предметы можно добавить сюда при необходимости
}


# Параметры кривой выпадения (используются при выборе предмета из кейса)
# DROP_RARE_POWER: чем больше значение, тем сильнее различие между
# common и rare — редкие предметы становятся ещё реже.
# DROP_MIN_WEIGHT: нижняя граница веса предмета (чтобы шанс никогда не был нулевым).
# DROP_WEIGHT_MULTIPLIER: глобальный множитель весов (удобно для быстрого масштабирования).
# Формула используемая в сцене открытия: weight = max(DROP_MIN_WEIGHT, (1.0 if rare<=0 else 1.0 / (rare ** DROP_RARE_POWER)) * DROP_WEIGHT_MULTIPLIER)
DROP_RARE_POWER: float = 1.5
DROP_MIN_WEIGHT: float = 0.0005
DROP_WEIGHT_MULTIPLIER: float = 1.0
