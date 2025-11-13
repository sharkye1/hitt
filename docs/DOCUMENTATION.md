# PROJECT DOCUMENTATION / ДОКУМЕНТАЦИЯ

This file contains a complete, structured documentation in Russian (first) and English (second).
It explains installation, usage, data formats, internals, and contribution guidelines for the Case Simulator project.

---

# Оглавление / Contents

1. Русская часть (Russian)
   - Введение
   - Быстрый старт
   - Установка и окружение
   - Структура проекта
   - Модели данных: Item, Case, Inventory
   - Формат `presets.py` (как добавлять предметы / кейсы)
   - Система качества (quality)
   - Pricing и продажа предметов
   - Сохранение и экспорт / формат сохранения
   - Скрипт симуляции и отчёты
   - Разработка и тесты
   - Вклад и Pull Requests
   - Лицензия

2. English part
   - Introduction
   - Quick start
   - Installation & environment
   - Project structure
   - Data models: Item, Case, Inventory
   - `presets.py` format (adding items/cases)
   - Quality system
   - Pricing & selling items
   - Save format
   - Simulation script & reports
   - Development & tests
   - Contributing
   - License

---

## Русская часть

### Введение

Case Simulator — локальный консольный проект для моделирования открытия кейсов, управления инвентарём и витриной магазина.
Цели проекта:
- Быстро тестировать игровые экономики (цены, редкости, шансы).
- Анализировать статистику выпадений и качество предметов.
- Поддерживать пер-instance качества предметов (качество каждой копии отдельно).

Проект ориентирован на разработчиков/исследователей, которые хотят экспериментировать с набором предметов и шансами выпадений.

### Быстрый старт

1. Клонируйте репозиторий и перейдите в папку проекта:

```powershell
git clone <repo-url>
cd hitt
```

2. (Опционально) создайте виртуальное окружение и активируйте его:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Запустите игру (интерактивная консольная программа):

```powershell
python main.py
```

4. Быстрая симуляция выпадений и генерация отчёта:

```powershell
python scripts/run_simulation.py
```

> Примечание: для быстрой проверки уменьшите `trials` внутри скрипта (например, 100_000).

### Установка и окружение

В текущей версии проект использует только стандартную библиотеку Python. Если в будущем появятся зависимости — они будут описаны в `requirements.txt` или `pyproject.toml`.

### Структура проекта

Ключевые файлы/папки:

- `main.py` — входная точка (CLI)
- `case_simulator/app.py` — инициализация приложения и регистрация сцен
- `case_simulator/models/` — определения классов `Item`, `Case`, `Inventory`
- `case_simulator/scenes/` — сцены: `main_menu`, `case_opening`, `shop`, `inventory` и т.д.
- `case_simulator/utils/` — утилиты: `quality.py`, `pricing.py`, `console.py` и т.п.
- `case_simulator/data/presets.py` — контент: определения `Item` и `Case`
- `case_simulator/save_manager.py` — логика сохранения/загрузки состояния
- `scripts/run_simulation.py` — генерация статистических отчётов по выпадениям
- `tools/simulate_drops.py` — ядро симуляции / алгоритмы выборки
- `reports/` — (опционально) папка для сохранения отчётов симуляции

### Модели данных

Краткое описание основных моделей (свойства и назначение).

Item
- id: str — уникальный идентификатор
- name: str — отображаемое имя
- price: int — базовая цена
- category: str — категория (например, 'pistol', 'rifle', 'knife')
- rare: int — целочисленный показатель редкости (опционально, влияет на шансы/витрину)
- validation: при создании валидируется, что quality ∈ [0.0, 1.0] (если указывается)

Case
- id: str — уникальный идентификатор кейса
- name: str — отображаемое название
- price: int — цена кейса
- items: tuple[Item, ...] — набор предметов, которые могут выпасть из кейса

Inventory
- хранит кейсы и предметы игрока
- для предметов используется per-instance хранение качества: каждая копия предмета связана со значением quality (float)

### Формат `presets.py` и добавление контента

`presets.py` содержит объявления Item/Case, а также логику автоматической агрегации `ITEMS` и `CASES`.

Рекомендации:
- Объявляйте `Item` переменные в верхней части файла перед блоком автоматического сбора.
- Для кейсов создавайте либо вручную `Case(...)`, либо используйте предоставленные утилиты/группировки.

Примеры:

```python
MY_GUN = Item(id="m_gun", name="Training Gun", price=500, category="pistol", rare=2)
MY_CASE = Case(id="my_case", name="Training Case", price=150, items=(MY_GUN,))
```

Автоматическая агрегация собирает все глобальные переменные типа `Item` в список `ITEMS` и `Case` в `CASES`.

Если вы хотите гарантировать, что ваш новый Item будет включён, объявляйте его до кода, который выполняет сбор. Альтернатива — переместить сбор в конец файла (я могу изменить это по запросу).

### Система качества (quality)

- `quality` — float в диапазоне [0.0, 1.0], с 6 знаками точности.
- Генерируется при выпадении предмета через `case_simulator/utils/quality.py::gen_quality()`.
- Алгоритм основывается на beta-распределении с дополнительными редкими бэндами для хвостов распределения.
- Редкие бэнды по умолчанию: >=0.99, >=0.9951, >=0.9990.
- Значение `quality` используется в расчёте итоговой цены: `price = base_price * price_multiplier(q)`.

Примечание по тюнингу: чтобы сместить среднее или изменить хвосты распределения, скорректируйте параметры beta в `quality.py`.

### Система крафта (Crafting)

В проект добавлена система крафта предметов — её назначение и ключевые правила:

- Режимы: probabilistic (вероятностный апгрейд), deterministic (гарантированный обмен/слияние), fusion (слияние нескольких предметов в новый) и upgrade (попытка улучшить предмет).
- При попытке крафта входные предметы удаляются (сгорают). В режимах с вероятностью неуспеха, при неудаче новый предмет не создаётся и входы теряются.
- Если все выбранные предметы принадлежат к одной категории, итог будет ограничен этой категорией.
- Итоговый предмет получает сгенерированное `quality` — качество входных предметов не переносится на новый предмет напрямую.
- Выбор шаблона результата учитывает скорректированную цену (adjusted price = base_price * price_multiplier(q)), причём при подборе шаблона используется именно сгенерированное качество выходного предмета.
- Стоимость крафта вычисляется как 0.2% от суммы скорректированных цен входов: cost = max(1, round(adjusted_sum * 0.002)). Минимальная стоимость — 1 единица.
- В интерфейсе для выбора предметов показывается только скорректированная цена (adj) и качество; id и базовая цена скрыты.
- После успешного крафта созданный предмет добавляется в инвентарь; при неуспехе предмет не добавляется (входы уже удалены).
- Перед выбором режима в интерфейсе доступен краткий гайд по режимам (пункт "гайд"), объясняющий отличия и риски.

Рекомендуется запускать симуляции и тесты при тюнинге параметров крафта, чтобы оценить влияние на экономику и распределение качеств.

### Pricing и продажа предметов

- Реализована функция `price_multiplier(q)` в `case_simulator/utils/pricing.py`, которая преобразует `quality` в множитель цены.
- При продаже конкретной копии предмета используется её `quality`.
- При выборе продажи в интерфейсе игрок получает процент от расчётной цены (например, 80%) — смотрите логику в сцене продажи.

### Сохранение/формат сохранения

- `SaveManager` сохраняет `GameState`, включая баланс, инвентарь и `granted_presets`.
- Формат — JSON, возможно с кодированием/шифрованием (см. реализацию в `save_manager.py`).
- В инвентаре предметы сохраняются вместе со списком их `quality` (список качеств для каждой копии конкретного id).

### Скрипт симуляции и отчёты

- `scripts/run_simulation.py` использует `tools/simulate_drops.simulate()`.
- Скрипт выводит и может сохранить файл отчёта со следующими метриками:
  - trials — число симуляций
  - Ожидаемое распределение по предметам (weight-based)
  - Эмпирическое распределение (количества и вероятности)
  - Среднее и std `quality` по предмету
  - Счётчики попаданий в редкие бэнды
- Отчёты сохраняются в `reports/drop_report_<timestamp>.txt` (если скрипт настроен на запись).

### Разработка и тесты

Рекомендую добавить:
- `requirements.txt` (если появятся внешние пакеты)
- GitHub Actions workflow для автотестов и/или симуляций
- Unit-tests (pytest) для:
  - генератора quality
  - функции price_multiplier
  - основных моделей (создание Item/Case/Inventory)

### Вклад

1. Fork the repo
2. Create a feature branch
3. Add tests and changes
4. Open a Pull Request with description and (if applicable) a sample report from `scripts/run_simulation.py` that demonstrates the effect of your change

### Лицензия

Добавьте файл `LICENSE` в корень репозитория. Рекомендуется MIT.

---

## English part

### Introduction

Case Simulator is a small local console project to simulate case openings, inventory management and a shop.
It is designed to:
- Quickly test economy changes (prices, rarities, probabilities)
- Analyze drop statistics and per-instance item quality
- Help development and balancing of case/item systems

### Quick start

1. Clone repo and cd into project:

```powershell
git clone <repo-url>
cd hitt
```

2. (Optional) Create and activate virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Run the game (console app):

```powershell
python main.py
```

4. Run a simulation to generate drop report:

```powershell
python scripts/run_simulation.py
```

Notes: reduce `trials` in the script for a quick run (e.g. 100_000), or use 1_000_000+ for more stable statistics.

### Installation & environment

Currently no external dependencies are required. If dependencies are added, they will be listed in `requirements.txt` or `pyproject.toml`.

### Project structure

Key files/folders:

- `main.py` — entry point
- `case_simulator/app.py` — app initialization and scenes
- `case_simulator/models/` — Item, Case, Inventory
- `case_simulator/scenes/` — menu, case_opening, shop, inventory
- `case_simulator/utils/` — helpers: quality.py, pricing.py, console
- `case_simulator/data/presets.py` — content definitions (items, cases)
- `case_simulator/save_manager.py` — save/load logic
- `scripts/run_simulation.py` — run simulation and save human-readable reports
- `tools/simulate_drops.py` — simulation core

### Data models: Item, Case, Inventory

Item
- id: string — unique identifier
- name: string — display name
- price: int — base price
- category: string — e.g. 'pistol', 'rifle'
- rare: int — integer rarity tier

Case
- id: string
- name: string
- price: int
- items: tuple of Item

Inventory
- stores cases and items
- items keep per-instance qualities (array of qualities for each copy)

### `presets.py` format (adding items and cases)

Add `Item` objects as global variables. The module aggregates them into `ITEMS` and `CASES` automatically.

Example:

```python
MY_GUN = Item(id="my_gun", name="My Gun", price=1200, category="pistol", rare=3)
MY_CASE = Case(id="my_case", name="My Case", price=250, items=(MY_GUN,))
```

If you need to guarantee aggregation, define items before the aggregation code block or request to move aggregation to the end of the file.

### Quality system

- `quality` is a float in [0.0, 1.0] with 6 decimal places.
- Generated via `case_simulator/utils/quality.py::gen_quality()` using a beta-distribution with rare tail bands.
- Rare bands: >=0.99, >=0.9951, >=0.9990.
- Quality affects price via `price_multiplier(q)` in `case_simulator/utils/pricing.py`.

Tune beta parameters in `quality.py` to adjust mean or tail behavior.

### Pricing and selling

- Use `price_multiplier(q)` to compute multiplier from quality.
- Selling a specific copy of an item uses its assigned `quality`.
- GUI/CLI sale flows apply configured percentages (e.g. 80% of computed price) — check scenes for exact numbers.

### Save format

- `SaveManager` persists game state including balance, inventory, and granted presets.
- Format: JSON (possibly encoded) — see `save_manager.py` implementation.
- Inventory entries include arrays of per-instance qualities.

### Simulation and reports

- `scripts/run_simulation.py` runs `tools/simulate_drops.simulate()` and outputs a report with:
  - trials
  - expected vs empirical probabilities per item
  - mean and std of qualities per item
  - counts for rare bands

- The script writes `reports/drop_report_<timestamp>.txt` (if enabled) and prints a summary to console.

### Development and testing

Suggestions:
- Add `requirements.txt` and CI workflows (GitHub Actions) to run tests and sample simulations.
- Add unit tests (pytest) for quality generation, pricing, and data models.

Simple smoke test for content changes:

```powershell
python -c "import importlib; m=importlib.import_module('case_simulator.data.presets'); print('ITEMS=', len(m.ITEMS), 'CASES=', [c.id for c in m.CASES])"
```

### Contributing

1. Fork the repository
2. Create a descriptive branch
3. Add code and tests
4. Open a Pull Request and include a short report (if the change affects probabilities/economy)

### License

Add `LICENSE` to the repository root. MIT is recommended.

---

If you want, I can split this into separate `docs/ru/*` and `docs/en/*` files, generate a Table of Contents, or add cross-links and examples (how to add 10 new pistols and split them into 3 cases automatically). Tell me which format you prefer.
