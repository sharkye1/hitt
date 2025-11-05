from __future__ import annotations

from case_simulator.models.item import Item
from case_simulator.models.case import Case
from case_simulator.models.inventory import Inventory


# Примеры предметов
PISTOL_MK1 = Item(id="pistol_mk1", name="Pistol Mk1", price=100, category="weapon", rare=1)
KNIFE_RUSTY = Item(id="knife_rusty", name="Rusty Knife", price=250, category="knife", rare=2)
RIFLE_PRO = Item(id="rifle_pro", name="Rifle Pro", price=500, category="weapon", rare=3)
SHOTGUN_HEAVY = Item(id="shotgun_heavy", name="Shotgun Heavy", price=450, category="weapon", rare=4)
ULTIMATE_SWORD = Item(id="ultimate_sword", name="Ultimate Sword", price=1000, category="melee", rare=5)


# Примеры кейсов (каждый содержит по паре предметов)
STARTER_CASE = Case(
    id="starter_case",
    name="Starter Case",
    price=150,
    items=(PISTOL_MK1, KNIFE_RUSTY),
)

PRO_CASE = Case(
    id="pro_case",
    name="Pro Case",
    price=400,
    items=(RIFLE_PRO, SHOTGUN_HEAVY),
)

ULTIMATE_CASE = Case(
    id="ultimate_case",
    name="Ultimate Case",
    price=1000,
    items=(PISTOL_MK1, KNIFE_RUSTY, RIFLE_PRO, SHOTGUN_HEAVY, ULTIMATE_SWORD)
)


def create_sample_inventory() -> Inventory:
    inv = Inventory()

    # Зарегистрируем шаблоны (на будущее, если добавятся новые дропы)
    for item in (PISTOL_MK1, KNIFE_RUSTY, RIFLE_PRO, SHOTGUN_HEAVY):
        inv.register_item(item)
    for case in (STARTER_CASE, PRO_CASE):
        inv.register_case(case)

    # NOTE: Не добавляем стартовые количества кейсов здесь. Стартовые/подарочные
    # контролируются FREE_PRESET_CASES (ниже) и предоставляются
    # SaveManager при создании нового сохранения или при появлении новых пресетов.

    # Мы храним пару стартовых предметов в каталоге, но не мутируем
    # постоянные количества здесь (так что предоставление может быть выполнено в одном месте).
    inv.register_item(PISTOL_MK1)
    inv.register_item(KNIFE_RUSTY)

    return inv


# Сопоставление case_id -> qty, которое должно быть выдано один раз каждому игроку, когда
# кейс будет представлен в `presets.py`. Добавляйте новые записи здесь, когда добавляете
# новые бесплатные/промо-кейсы в репозиторий. SaveManager гарантирует, что каждый
# id из этого сопоставления будет добавлен в инвентарь игрока не более одного раза.
FREE_PRESET_CASES: dict[str, int] = {
    # existing starter freebies
    "starter_case": 2,
    "pro_case": 1,
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
    # продаём также оба стартовых кейса — starter бесплатен для новых игроков, но
    # также может продаваться в магазине (например, для дополнительных копий)
    "starter_case": {"type": "case", "price": 120, "stock": None},
    "pro_case": {"type": "case", "price": 380, "stock": 5},
    "ultimate_case": {"type": "case", "price": 1000, "stock": 1},

    # некоторые предметы в магазине
    
}
