from __future__ import annotations

from case_simulator.models.item import Item
from case_simulator.models.case import Case
from case_simulator.models.inventory import Inventory


# Примеры предметов — расширенные: несколько пистолетов, винтовок, AWP и редкий нож
# Пистолеты (более частые)
PISTOL_MK1 = Item(id="pistol_mk1", name="Пистол мк1", price=100, category="pistol", rare=1)
PISTOL_MK2 = Item(id="pistol_mk2", name="Пистол мк2", price=140, category="pistol", rare=1)
PISTOL_MK3 = Item(id="pistol_mk3", name="Пистол мк3", price=180, category="pistol", rare=2)

# Винтовки (реже и дороже)
RIFLE_BASIC = Item(id="rifle_basic", name="Винтовка Базовая", price=450, category="rifle", rare=3)
RIFLE_PRO = Item(id="rifle_pro", name="Винтовка Про", price=650, category="rifle", rare=4)

# AWP — очень редкий и дорогой снайперский ски
AWP_LEGEND = Item(id="awp_legend", name="AWP Легенда", price=3000, category="sniper", rare=8)

# Ножи: один дешёвый и один легендарный (для knife-case)
KNIFE_RUSTY = Item(id="knife_rusty", name="Кухонный нож", price=250, category="knife", rare=2)
KNIFE_LEGEND = Item(id="knife_legend", name="Легендарный нож", price=8000, category="knife", rare=10)


# Коллекции предметов и кейсов — удобно итерации и быстрый доступ по id
# Дополнительные дорогие предметы (много штук): пистолеты, USP, Deagle, мини/обычные дробаши, винтовки, AWP-ы и ножи
PISTOL_USP = Item(id="usp_standard", name="USP Standard", price=1200, category="pistol", rare=5)
PISTOL_USP_SILVER = Item(id="usp_silver", name="USP Silver", price=1800, category="pistol", rare=6)
PISTOL_USP_GOLD = Item(id="usp_gold", name="USP Gold", price=3200, category="pistol", rare=8)

DEAGLE_BASIC = Item(id="deagle_basic", name="Desert Eagle", price=900, category="pistol", rare=5)
DEAGLE_GOLD = Item(id="deagle_gold", name="Desert Eagle Gold", price=2400, category="pistol", rare=7)
DEAGLE_ELITE = Item(id="deagle_elite", name="Desert Eagle Elite", price=4200, category="pistol", rare=9)

PISTOL_1911 = Item(id="pistol_1911", name="1911 Classic", price=800, category="pistol", rare=4)
PISTOL_PREMIUM = Item(id="pistol_premium", name="Premium Pistol", price=1500, category="pistol", rare=6)

# Мини-дробаши
MINI_SG1 = Item(id="mini_sg1", name="Mini Shotgun I", price=700, category="shotgun", rare=4)
MINI_SG2 = Item(id="mini_sg2", name="Mini Shotgun II", price=1200, category="shotgun", rare=5)

# Обычные дробаши
SG_BASIC = Item(id="sg_basic", name="Shotgun Basic", price=1500, category="shotgun", rare=6)
SG_HEAVY = Item(id="sg_heavy", name="Shotgun Heavy", price=2600, category="shotgun", rare=7)

# Новые винтовки
RIFLE_ELITE = Item(id="rifle_elite", name="Rifle Elite", price=1200, category="rifle", rare=5)
RIFLE_PREMIUM = Item(id="rifle_premium", name="Rifle Premium", price=2200, category="rifle", rare=7)
RIFLE_SUPER = Item(id="rifle_super", name="Rifle Super", price=4800, category="rifle", rare=10)
AK47_GOLD = Item(id="ak47_gold", name="AK-47 Gold", price=9000, category="rifle", rare=12)

# AWP-варинты
AWP_GOLD = Item(id="awp_gold", name="AWP Gold", price=5000, category="sniper", rare=12)
AWP_DRAGON = Item(id="awp_dragon", name="AWP Dragon", price=12000, category="sniper", rare=15)

# Множество ножей — дорогие
KNIFE_TACTICAL = Item(id="knife_tactical", name="Tactical Knife", price=9000, category="knife", rare=11)
KNIFE_BUTTERFLY = Item(id="knife_butterfly", name="Butterfly Knife", price=18000, category="knife", rare=18)
KNIFE_OBSIDIAN = Item(id="knife_obsidian", name="Obsidian Knife", price=20000, category="knife", rare=20)
KNIFE_SHADOW = Item(id="knife_shadow", name="Shadow Knife", price=15000, category="knife", rare=16)
KNIFE_CERAMIC = Item(id="knife_ceramic", name="Ceramic Knife", price=12000, category="knife", rare=14)

# Добавим всё в коллекцию ITEMS
# Cheap / budget-tier items (named variables so we can reference them in cases)
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

ITEMS = (
    # уникальные шмотки
    KAI_BOOTS,
    MICE_PANTS,
    VIPERR_TOUR_SHIRT1,
    VIPERR_TOUR_SHIRT2,
    VIPERR_TOUR_SHIRT3,

    # cheap tier
    PISTOL_BASIC_CHEAP,
    PISTOL_TRAINER,
    USP_BUDGET,
    DEAGLE_OLD,
    POCKET_1911,
    MINI_SHOT_CHEAP,
    BUCK_SHOT,
    RIFLE_WOOD,
    RIMFIRE,
    POCKET_AWM,
    KNIFE_PAPER,
    KNIFE_PLASTIC,
    KNIFE_CHEAP_FIXED,

    # original items and mid/high tier
    PISTOL_MK1,
    PISTOL_MK2,
    PISTOL_MK3,
    RIFLE_BASIC,
    RIFLE_PRO,
    AWP_LEGEND,
    KNIFE_RUSTY,
    KNIFE_LEGEND,
    # pistols
    PISTOL_USP,
    PISTOL_USP_SILVER,
    PISTOL_USP_GOLD,
    DEAGLE_BASIC,
    DEAGLE_GOLD,
    DEAGLE_ELITE,
    PISTOL_1911,
    PISTOL_PREMIUM,
    # shotguns
    MINI_SG1,
    MINI_SG2,
    SG_BASIC,
    SG_HEAVY,
    # rifles
    RIFLE_ELITE,
    RIFLE_PREMIUM,
    RIFLE_SUPER,
    AK47_GOLD,
    # awps
    AWP_GOLD,
    AWP_DRAGON,
    # knives
    KNIFE_TACTICAL,
    KNIFE_BUTTERFLY,
    KNIFE_OBSIDIAN,
    KNIFE_SHADOW,
    KNIFE_CERAMIC,
)

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

PISTOL_CASE = Case(
    id="pistol_case",
    name="Pistol Case",
    price=120,
    items=(
        PISTOL_BASIC_CHEAP,
        PISTOL_TRAINER,
        POCKET_1911,
        PISTOL_MK1,
        PISTOL_MK2,
        PISTOL_MK3,
        PISTOL_1911,
        USP_BUDGET,
        PISTOL_USP,
        DEAGLE_BASIC,
        DEAGLE_OLD,
        PISTOL_PREMIUM,
    ),
)

RIFLE_CASE = Case(
    id="rifle_case",
    name="Rifle Case",
    price=400,
    items=(
        RIFLE_WOOD,
        RIMFIRE,
        RIFLE_BASIC,
        RIFLE_PRO,
        RIFLE_ELITE,
        RIFLE_PREMIUM,
        SG_BASIC,
        SG_HEAVY,
    ),
)

AWP_CASE = Case(
    id="awp_case",
    name="AWP Case",
    price=2500,
    items=(
        POCKET_AWM,
        AWP_LEGEND,
        AWP_GOLD,
        AWP_DRAGON,
        RIFLE_SUPER,
        AK47_GOLD,
        PISTOL_PREMIUM,
    ),
)

KNIFE_CASE = Case(
    id="knife_case",
    name="Knife Case",
    price=10000,
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

CASES = (PISTOL_CASE, 
         RIFLE_CASE, 
         AWP_CASE, 
         KNIFE_CASE, 
         VIPERR_CASE)


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
