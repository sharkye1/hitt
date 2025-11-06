from __future__ import annotations

from case_simulator.models.item import Item
from case_simulator.models.case import Case
from case_simulator.models.inventory import Inventory

# Пистолетики
PISTOL_MK1 = Item(id="pistol_mk1", name="Пистолет мак1", price=100, category="pistol", rare=1)
PISTOL_MK2 = Item(id="pistol_mk2", name="Пистолет мак2", price=140, category="pistol", rare=1)
PISTOL_MK3 = Item(id="pistol_mk3", name="Пистолет мак3", price=180, category="pistol", rare=2)
PISTOL_MK4 = Item(id="pistol_mk4", name="Мак4 Epic", price=300, category="pistol", rare=4)
PISTOL_MK5 = Item(id="pistol_mk5", name="Мак5 Legendary", price=500, category="pistol", rare=8)


# Эмочки
M4A1_SILVER = Item(id="m4a1_silver", name="M4A1 Silver", price=1200, category="rifle", rare=6)
M4A1_GOLD = Item(id="m4a1_gold", name="M4A1 Gold", price=2500, category="rifle", rare=9)
M4A1_PLATINUM = Item(id="m4a1_platinum", name="M4A1 Platinum", price=5000, category="rifle", rare=12)
M4A1_DIAMOND = Item(id="m4a1_diamond", name="M4A1 Diamond", price=8000, category="rifle", rare=15)
M4A1_ULTIMATE = Item(id="m4a1_ultimate", name="M4A1 Ultimate", price=12000, category="rifle", rare=18)
M4A1_EXTREME = Item(id="m4a1_extreme", name="M4A1 Extreme", price=15000, category="rifle", rare=20)
M4A1_HYPER = Item(id="m4a1_hyper", name="M4A1 Hyper", price=20000, category="rifle", rare=25)
M4A1_TITANIUM = Item(id="m4a1_titanium", name="M4A1 Titanium", price=25000, category="rifle", rare=30)
M4A1_MEGALODON = Item(id="m4a1_megalodon", name="M4A1 Megalodon", price=30000, category="rifle", rare=35) 
M4A1_CELESTIAL = Item(id="m4a1_celestial", name="M4A1 Celestial", price=40000, category="rifle", rare=40)
M4A1_GALAXY = Item(id="m4a1_galaxy", name="M4A1 Galaxy", price=50000, category="rifle", rare=45)
M4A1_COSMIC = Item(id="m4a1_cosmic", name="M4A1 Cosmic", price=60000, category="rifle", rare=50)
M4A1_NEBULA = Item(id="m4a1_nebula", name="M4A1 Nebula", price=70000, category="rifle", rare=55)
M4A1_SUPREME = Item(id="m4a1_supreme", name="M4A1 Supreme", price=80000, category="rifle", rare=60)
M4A1_ULTIMATE_PLUS = Item(id="m4a1_ultimate_plus", name="M4A1 Ultimate Plus", price=90000, category="rifle", rare=65)
M4A1_OMEGA = Item(id="m4a1_omega", name="M4A1 Omega", price=100000, category="rifle", rare=70)
M4A1_INFINITY = Item(id="m4a1_infinity", name="M4A1 Infinity", price=120000, category="rifle", rare=75)
M4A1_ETERNAL = Item(id="m4a1_eternal", name="M4A1 Eternal", price=150000, category="rifle", rare=80)
M4A1_DIVINE = Item(id="m4a1_divine", name="M4A1 Divine", price=200000, category="rifle", rare=90)
M4A1_TRANSCENDENT = Item(id="m4a1_transcendent", name="M4A1 Transcendent", price=300000, category="rifle", rare=100)

# Калашики
AK47_WOODEN = Item(id="ak47_wooden", name="AK-47 Wooden", price=1500, category="rifle", rare=7)
AK47_CAMO = Item(id="ak47_camo", name="AK-47 Camo", price=2800, category="rifle", rare=10)
AK47_FOREST = Item(id="ak47_forest", name="AK-47 Forest", price=4500, category="rifle", rare=13)
AK47_ROUBINET = Item(id="ak47_roubinet", name="AK-47 Roubinet", price=7000, category="rifle", rare=16)
AK47_CRIMSON = Item(id="ak47_crimson", name="AK-47 Crimson", price=10000, category="rifle", rare=20)
AK47_PHANTOM = Item(id="ak47_phantom", name="AK-47 Phantom", price=15000, category="rifle", rare=25)
AK47_TITANIUM = Item(id="ak47_titanium", name="AK-47 Titanium", price=20000, category="rifle", rare=30)
AK47_WINTER = Item(id="ak47_winter", name="AK-47 Winter", price=25000, category="rifle", rare=35)
AK47_PONCHIO = Item(id="ak47_ponchio", name="AK-47 Ponchio", price=30000, category="rifle", rare=40)
AK47_DREADNOUGHT = Item(id="ak47_dreadnought", name="AK-47 Dreadnought", price=40000, category="rifle", rare=45)
AK47_PHANTASMAGORIA = Item(id="ak47_phantasmagoria", name="AK-47 Phantasmagoria", price=50000, category="rifle", rare=50)
AK47_CELESTIAL = Item(id="ak47_celestial", name="AK-47 Celestial", price=60000, category="rifle", rare=55)
AK47_PLASMAPHONIA = Item(id="ak47_plasmaphonia", name="AK-47 Plasmaphonia", price=70000, category="rifle", rare=60)

# Авики 
AWP_FISH = Item(id="awp_fish", name="AWP Рыбка", price=100, category="sniper", rare=7)
AWP_FIRE = Item(id="awp_fire", name="AWP Огонь", price=2000, category="sniper", rare=8)
AWP_LEGEND = Item(id="awp_legend", name="AWP Легенда", price=3000, category="sniper", rare=10)
AWP_MONSTER = Item(id="awp_monster", name="AWP Монстр", price=8000, category="sniper", rare=12)
AWP_HYPERIOUS = Item(id="awp_hyperious", name="AWP Гипериус", price=15000, category="sniper", rare=15)
AWP_VAIPOROUS = Item(id="awp_vaporous", name="AWP Паровой", price=25000, category="sniper", rare=25)
AWP_MECTICUS = Item(id="awp_mecticus", name="AWP Мектикус", price=40000, category="sniper", rare=40)
AWP_BARABANIUS = Item(id="awp_barabanius", name="AWP Барабаниус", price=60000, category="sniper", rare=55)
AWP_ORTEGA = Item(id="awp_ortega", name="AWP Ортега", price=80000, category="sniper", rare=60)

# Ножи: один дешёвый и один легендарный (для knife-case)
KNIFE_RUSTY = Item(id="knife_rusty", name="Кухонный нож", price=250, category="knife", rare=1)
KNIFE_METALLIC = Item(id="knife_metallic", name="Металлический нож", price=500, category="knife", rare=3)
KNIFE_BEDEND = Item(id="knife_bedend", name="Нож Беденд", price=750, category="knife", rare=5)
KNIFE_LEGEND = Item(id="knife_legend", name="Легендарный нож", price=8000, category="knife", rare=10)
KNIFE_TACTICAL = Item(id="knife_tactical", name="Тактический нож", price=9000, category="knife", rare=11)
KNIFE_CERAMIC = Item(id="knife_ceramic", name="Керамический нож", price=12000, category="knife", rare=14)
KNIFE_SHADOW = Item(id="knife_shadow", name="Нож Тени", price=15000, category="knife", rare=16)
KNIFE_BUTTERFLY = Item(id="knife_butterfly", name="Нож Бабочка", price=18000, category="knife", rare=18)
KNIFE_OBSIDIAN = Item(id="knife_obsidian", name="Нож Обсидиан", price=20000, category="knife", rare=20)

# Коллекции предметов и кейсов — удобно итерации и быстрый доступ по id
# Дополнительные дорогие предметы (много штук): пистолеты, USP, Deagle, мини/обычные дробаши, винтовки, AWP-ы и ножи
PISTOL_USP = Item(id="usp_standard", name="USP Стандарт", price=1200, category="pistol", rare=5)
PISTOL_USP_SILVER = Item(id="usp_silver", name="USP Серебро", price=1800, category="pistol", rare=6)
PISTOL_USP_GOLD = Item(id="usp_gold", name="USP Золото", price=3200, category="pistol", rare=8)
PISTOL_USP_PLATINUM = Item(id="usp_platinum", name="USP Платина", price=6000, category="pistol", rare=10)
PISTOL_USP_DIAMOND = Item(id="usp_diamond", name="USP Бриллиант", price=10000, category="pistol", rare=12)
PISTOL_USP_ULTIMATE = Item(id="usp_ultimate", name="USP Ультимейт", price=15000, category="pistol", rare=15)
PISTOL_USP_EXTREME = Item(id="usp_extreme", name="USP Экстрим", price=20000, category="pistol", rare=18)
PISTOL_USP_HYPER = Item(id="usp_hyper", name="USP Гипер", price=25000, category="pistol", rare=20)
PISTOL_USP_TITANIUM = Item(id="usp_titanium", name="USP Титаниум", price=30000, category="pistol", rare=25)
PISTOL_USP_MEGALODON = Item(id="usp_megalodon", name="USP Мегалодон", price=40000, category="pistol", rare=30)
PISTOL_USP_CELESTIAL = Item(id="usp_celestial", name="USP Целестиал", price=50000, category="pistol", rare=35)
PISTOL_USP_GALAXY = Item(id="usp_galaxy", name="USP Гэлакси", price=60000, category="pistol", rare=40)
PISTOL_USP_COSMIC = Item(id="usp_cosmic", name="USP Космик", price=70000, category="pistol", rare=45)
PISTOL_USP_NEBULA = Item(id="usp_nebula", name="USP Небула", price=80000, category="pistol", rare=50)
PISTOL_USP_SUPREME = Item(id="usp_supreme", name="USP Суприм", price=90000, category="pistol", rare=55)
PISTOL_USP_ULTIMATE_PLUS = Item(id="usp_ultimate_plus", name="USP Ультимейт Плюс", price=100000, category="pistol", rare=60)


DEAGLE = Item(id="deagle_basic", name="Desert Eagle", price=900, category="pistol", rare=5)
DEAGLE_SILVER = Item(id="deagle_silver", name="Desert Eagle Silver", price=1600, category="pistol", rare=7)
DEAGLE_GOLD = Item(id="deagle_gold", name="Desert Eagle Gold", price=2800, category="pistol", rare=9)
DEAGLE_PLATINUM = Item(id="deagle_platinum", name="Desert Eagle Platinum", price=4500, category="pistol", rare=11)
DEAGLE_DIAMOND = Item(id="deagle_diamond", name="Desert Eagle Diamond", price=7000, category="pistol", rare=13)
DEAGLE_ULTIMATE = Item(id="deagle_ultimate", name="Desert Eagle Ultimate", price=9000, category="pistol", rare=15)
DEAGLE_EXTREME = Item(id="deagle_extreme", name="Desert Eagle Extreme", price=12000, category="pistol", rare=18)
DEAGLE_HYPER = Item(id="deagle_hyper", name="Desert Eagle Hyper", price=15000, category="pistol", rare=20)
DEAGLE_TITANIUM = Item(id="deagle_titanium", name="Desert Eagle Titanium", price=20000, category="pistol", rare=25)
DEAGLE_MEGALODON = Item(id="deagle_megalodon", name="Desert Eagle Megalodon", price=30000, category="pistol", rare=30)
DEAGLE_CELESTIAL = Item(id="deagle_celestial", name="Desert Eagle Celestial", price=40000, category="pistol", rare=35)
DEAGLE_GALAXY = Item(id="deagle_galaxy", name="Desert Eagle Galaxy", price=50000, category="pistol", rare=40)
DEAGLE_COSMIC = Item(id="deagle_cosmic", name="Desert Eagle Cosmic", price=60000, category="pistol", rare=45)
DEAGLE_NEBULA = Item(id="deagle_nebula", name="Desert Eagle Nebula", price=70000, category="pistol", rare=50)
DEAGLE_SUPREME = Item(id="deagle_supreme", name="Desert Eagle Supreme", price=80000, category="pistol", rare=55)
DEAGLE_ULTIMATE_PLUS = Item(id="deagle_ultimate_plus", name="Desert Eagle Ultimate Plus", price=90000, category="pistol", rare=60)




PISTOL_1911 = Item(id="pistol_1911", name="1911 Classic", price=800, category="pistol", rare=4)
PISTOL_PREMIUM = Item(id="pistol_premium", name="Premium Pistol", price=1500, category="pistol", rare=6)

# Мини-дробаши
MINI_SG1 = Item(id="mini_sg1", name="Mini Shotgun I", price=700, category="shotgun", rare=4)
MINI_SG2 = Item(id="mini_sg2", name="Mini Shotgun II", price=1200, category="shotgun", rare=5)

# Обычные дробаши
SG_BASIC = Item(id="sg_basic", name="Shotgun Basic", price=1500, category="shotgun", rare=6)
SG_HEAVY = Item(id="sg_heavy", name="Shotgun Heavy", price=2600, category="shotgun", rare=7)




# Добавим всё в коллекцию ITEMS
# Дешевые / бюджетные 
PISTOL_BASIC_CHEAP = Item(id="pistol_basic_cheap", name="Pistol Basic Cheap", price=50, category="pistol", rare=1)
PISTOL_TRAINER = Item(id="pistol_trainer", name="Pistol Trainer", price=60, category="pistol", rare=1)
USP_BUDGET = Item(id="usp_budget", name="USP Budget", price=70, category="pistol", rare=1)
DEAGLE_OLD = Item(id="deagle_old", name="Deagle Old", price=80, category="pistol", rare=2)
POCKET_1911 = Item(id="pocket_1911", name="Pocket 1911", price=55, category="pistol", rare=1)
MINI_SHOT_CHEAP = Item(id="mini_shot_cheap", name="Mini Shotgun Cheap", price=90, category="shotgun", rare=1)
BUCK_SHOT = Item(id="buck_shot", name="Buck Shot", price=85, category="shotgun", rare=1)
RIFLE_WOOD = Item(id="rifle_wood", name="Rifle Wood", price=95, category="rifle", rare=2)
RIMFIRE = Item(id="rimfire", name="Rimfire", price=110, category="rifle", rare=2)
POCKET_AWM = Item(id="pocket_awm", name="Pocket AWM", price=130, category="sniper", rare=3)
# cheap knives
KNIFE_PAPER = Item(id="knife_paper", name="Paper Knife", price=40, category="knife", rare=1)
KNIFE_PLASTIC = Item(id="knife_plastic", name="Plastic Knife", price=45, category="knife", rare=1)
KNIFE_CHEAP_FIXED = Item(id="knife_cheap_fixed", name="Cheap Fixed Knife", price=60, category="knife", rare=2)

KAI_BOOTS = Item(id="kai_boots", name="Kai's Boots", price=1860, category="boots", rare=44)
MICE_PANTS = Item(id="mice_pants", name="Mice's Pants", price=1691, category="pants", rare=9)
VIPERR_TOUR_SHIRT1 = Item(id="viperr_tour_shirt_1", name="VIPERR Tour Тишка №1", price=3500, category="shirt", rare=15)
VIPERR_TOUR_SHIRT2 = Item(id="viperr_tour_shirt_2", name="VIPERR Tour Тишка №2", price=3500, category="shirt", rare=15)
VIPERR_TOUR_SHIRT3 = Item(id="viperr_tour_shirt_3", name="VIPERR Tour Тишка №3", price=3500, category="shirt", rare=15)

# Automatically collect all Item instances defined in this module into ITEMS.
# This avoids having to list every item variable manually. It preserves the
# definition order (module globals preserve insertion order in CPython).

# Автоматически собираем все экземпляры Item, определённые в этом модуле, в ITEMS.
# Это избавляет от необходимости перечислять каждую переменную вручную. Сохраняет
# порядок определения (глобалы модуля сохраняют порядок вставки в CPython).
_collected_items = []
for _name, _val in list(globals().items()):
    # we only want Item instances defined above (not Cases or other values)
    # мы хотим только экземпляры Item, определённые выше (не кейсы или другие значения)
    if isinstance(_val, Item):
        _collected_items.append(_val)

# Expose a public tuple `ITEMS` in the same shape as before
# Предоставляем публичный кортеж `ITEMS` в том же формате, что и раньше
ITEMS = tuple(_collected_items)

# clean up temporary name
# удаляем временное имя
del _collected_items

VIPERR_CASE = Case(
    id="viperr_case",
    name="VIPERR Case",
    price=3500,
    items=(
        KAI_BOOTS,
        MICE_PANTS
    ),
)



# Переопределяем (перераспределяем) содержимое кейсов, чтобы внутри каждого был
# сбалансированный набор: много бюджетных/частых + несколько редких дорогих.

# Build cases programmatically from existing items so every gun is placed
# into at least one case and specialty cases (M4A1/AK47/AWP) are provided.
# Helper: group items by category/prefix
_pistols = [it for it in ITEMS if getattr(it, "category", None) == "pistol"]
_rifles = [it for it in ITEMS if getattr(it, "category", None) == "rifle"]
_awps = [it for it in ITEMS if it.id.startswith("awp_")]
_m4a1s = [it for it in ITEMS if it.id.startswith("m4a1_")]
_ak47s = [it for it in ITEMS if it.id.startswith("ak47_")]
_shotguns = [it for it in ITEMS if getattr(it, "category", None) == "shotgun"]

def _avg_price(items_list: list) -> int:
    if not items_list:
        return 100
    return int(sum(getattr(i, "price", 0) for i in items_list) / len(items_list))

# Pistol case: include all pistols (evenly across if too many — keep them all here)
PISTOL_CASE = Case(
    id="pistol_case",
    name="Pistol Case",
    price=999,
    items=tuple(_pistols),
)

# M4A1 specialty case
if _m4a1s:
    M4A1_CASE = Case(
        id="m4a1_case",
        name="M4A1 Case",
        price=15000,
        items=tuple(_m4a1s),
    )

# AK47 specialty case
if _ak47s:
    AK47_CASE = Case(
        id="ak47_case",
        name="AK-47 Case",
        price=9200,
        items=tuple(_ak47s),
    )

# AWP case (snipers)
AWP_CASE = Case(
    id="awp_case",
    name="AWP Case",
    price=7100,
    items=tuple(_awps) if _awps else (POCKET_AWM, AWP_LEGEND),
)

# General rifle case: include rifles not in M4A1/AK47 groups
_rifles_remaining = [it for it in _rifles if it not in _m4a1s and it not in _ak47s]
RIFLE_CASE = Case(
    id="rifle_case",
    name="Rifle Case",
    price=100,
    items=tuple(_rifles_remaining or _rifles),
)

KNIFE_CASE = Case(
    id="knife_case",
    name="Knife Case",
    price=600,
    items=(
        KNIFE_PAPER,
        KNIFE_PLASTIC,
        KNIFE_CHEAP_FIXED,
        KNIFE_RUSTY,
        KNIFE_TACTICAL,
        KNIFE_LEGEND,
        KNIFE_BUTTERFLY,
        KNIFE_OBSIDIAN,
        KNIFE_SHADOW,
        KNIFE_CERAMIC,
    ),
)

_cases_list = [PISTOL_CASE, RIFLE_CASE, AWP_CASE, KNIFE_CASE, VIPERR_CASE]
_m4 = globals().get("M4A1_CASE")
if _m4 is not None:
    _cases_list.append(_m4)
_a47 = globals().get("AK47_CASE")
if _a47 is not None:
    _cases_list.append(_a47)

CASES = tuple(_cases_list)
del _cases_list


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
"""
SHOP_STOCK: формируется автоматически из списка `CASES`.
По умолчанию каждый case появляется в магазине с ценой, указанной в объекте Case,
и неограниченным запасом (stock=None). Здесь мы накладываем несколько явных
переопределений для редких/ограниченных кейсов.
"""

SHOP_STOCK: dict[str, dict] = {}

# Контроль: какие кейсы можно продавать в магазине.
# Если множество пустое, поведение по умолчанию — добавить все кейсы.
SELLABLE_CASE_IDS: set[str] = set()

for c in CASES:
    if SELLABLE_CASE_IDS and c.id not in SELLABLE_CASE_IDS:
        # пропускаем кейсы, которые не в белом списке
        continue
    SHOP_STOCK[c.id] = {"type": "case", "price": c.price, "stock": None}

# Контроль: какие отдельные предметы можно продавать в магазине.
# По умолчанию разрешаем только VIPERR Tour shirts — перечислите здесь id,
# которые вы хотите сделать доступными как отдельные товары.
SELLABLE_ITEM_IDS: set[str] = {
    "viperr_tour_shirt_1",
    "viperr_tour_shirt_2",
    "viperr_tour_shirt_3",
}

# Добавляем в магазин только те предметы из ITEMS, которые попали в whitelist.
for it in ITEMS:
    if it.id in SELLABLE_ITEM_IDS and it.id not in SHOP_STOCK:
        SHOP_STOCK[it.id] = {"type": "item", "price": it.price, "stock": None}


# Параметры кривой выпадения (используются при выборе предмета из кейса)
# DROP_RARE_POWER: чем больше значение, тем сильнее различие между
# common и rare — редкие предметы становятся ещё реже.
# DROP_MIN_WEIGHT: нижняя граница веса предмета (чтобы шанс никогда не был нулевым).
# DROP_WEIGHT_MULTIPLIER: глобальный множитель весов (удобно для быстрого масштабирования).
# Формула используемая в сцене открытия: weight = max(DROP_MIN_WEIGHT, (1.0 if rare<=0 else 1.0 / (rare ** DROP_RARE_POWER)) * DROP_WEIGHT_MULTIPLIER)
DROP_RARE_POWER: float = 1.5
DROP_MIN_WEIGHT: float = 0.0005
DROP_WEIGHT_MULTIPLIER: float = 1.0
