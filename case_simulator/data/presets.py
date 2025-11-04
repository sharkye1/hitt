from __future__ import annotations

from case_simulator.models.item import Item
from case_simulator.models.case import Case
from case_simulator.models.inventory import Inventory


# Примеры предметов
PISTOL_MK1 = Item(id="pistol_mk1", name="Pistol Mk1", price=100, category="weapon", rare=1)
KNIFE_RUSTY = Item(id="knife_rusty", name="Rusty Knife", price=250, category="knife", rare=2)
RIFLE_PRO = Item(id="rifle_pro", name="Rifle Pro", price=500, category="weapon", rare=3)
SHOTGUN_HEAVY = Item(id="shotgun_heavy", name="Shotgun Heavy", price=450, category="weapon", rare=4)

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


def create_sample_inventory() -> Inventory:
    inv = Inventory()

    # Зарегистрируем шаблоны (на будущее, если добавятся новые дропы)
    for item in (PISTOL_MK1, KNIFE_RUSTY, RIFLE_PRO, SHOTGUN_HEAVY):
        inv.register_item(item)
    for case in (STARTER_CASE, PRO_CASE):
        inv.register_case(case)

    # NOTE: do NOT add starter case counts here. Starter/gifted counts are
    # controlled by FREE_PRESET_CASES (below) and are granted by the
    # SaveManager when creating a fresh save or when new presets appear.

    # We keep a couple of starter items in the catalog but do not mutate
    # persistent counts here (so granting can be done in a single place).
    inv.register_item(PISTOL_MK1)
    inv.register_item(KNIFE_RUSTY)

    return inv


# Mapping of case_id -> qty that should be granted once to each player when
# the case is introduced in `presets.py`. Add new entries here when you add
# new free/promo cases in the repository. The SaveManager will ensure each
# id from this mapping is added to a player's inventory at most once.
FREE_PRESET_CASES: dict[str, int] = {
    # existing starter freebies
    "starter_case": 2,
    "pro_case": 1,
}
