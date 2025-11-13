from __future__ import annotations

import random
import time
from typing import Iterable, List, Optional, Tuple

from case_simulator.data import presets
from case_simulator.utils.quality import gen_quality
from case_simulator.utils.pricing import price_multiplier


# Tier definitions: user-selectable success chance tiers.
# Each tier defines a value multiplier that determines target prize value
# relative to the sum of adjusted input prices, and a boost probability
# which increases chance to get an ultra-rare quality outcome.
TIERS = {
    50: {"mult": 1.10, "boost": 0.001},
    35: {"mult": 1.6, "boost": 0.002},
    25: {"mult": 2.5, "boost": 0.005},
    10: {"mult": 6.0, "boost": 0.02},
}


def compute_adjusted_sum(items: Iterable[Tuple[str, float]]) -> float:
    """Compute sum of adjusted prices for selected items.

    items: iterable of (item_id, quality) tuples (qualities are per-instance).
    Uses `presets.ITEMS_BY_ID` to look up base price and `price_multiplier`.
    """
    s = 0.0
    for iid, q in items:
        template = presets.ITEMS_BY_ID.get(iid)
        if template is None:
            continue
        mult = price_multiplier(float(q)) if q is not None else 1.0
        s += template.price * mult
    return float(s)


def _quality_improvement_cap(avg_q: float) -> float:
    """Return a conservative improvement cap based on average input quality.

    This implements diminishing returns: higher avg_q gives smaller cap.
    """
    if avg_q < 0.8:
        return 0.08
    if avg_q < 0.9:
        return 0.05
    if avg_q < 0.95:
        return 0.03
    return 0.02


def generate_new_quality(avg_q: float, tier: int) -> float:
    """Generate a new quality for the crafted item.

    Guarantees new_q >= avg_q. The maximum improvement over avg_q is
    limited by `_quality_improvement_cap`. A small rare boost (tier-dependent)
    can replace the quality with a sampled `gen_quality()` result if that is
    larger than the base result.
    """
    cap = _quality_improvement_cap(avg_q)
    max_q = min(0.999999, avg_q + cap)

    # Base outcome: random in [avg_q, max_q]
    if max_q <= avg_q:
        base_q = avg_q
    else:
        base_q = random.uniform(avg_q, max_q)

    # Chance for a rare boost that may yield much higher q; tier lowers or
    # increases boost probability (lower-tier => larger boost chance)
    tier_info = TIERS.get(tier, TIERS[50])
    boost_p = tier_info.get("boost", 0.001)

    if random.random() < boost_p:
        boosted = gen_quality()
        # But respect the rule that final quality cannot be worse than avg_q
        final_q = max(avg_q, boosted)
        # and clamp
        final_q = min(final_q, 0.999999)
    else:
        final_q = base_q

    # Round to 6 decimals for consistency with other parts of the app
    return round(float(final_q), 6)


def select_output_template(target_value: float, new_quality: float, category: Optional[str] = None) -> Optional[Tuple[str, int]]:
    """Select an existing item template whose adjusted price (price * multiplier(new_quality))
    is close to the target_value.

    Returns (item_id, item_price) or None if nothing suitable found. If `category` is
    provided, candidate pool is restricted to that category.
    """
    # Consider only Items with price > 0
    candidates = [it for it in presets.ITEMS if it.price > 0]
    if category:
        candidates = [it for it in candidates if it.category == category]

    if not candidates:
        return None

    # Compute adjusted price for each candidate using price_multiplier(new_quality)
    mult = price_multiplier(float(new_quality))

    best = None
    best_diff = None
    for it in candidates:
        adjusted = it.price * mult
        diff = abs(adjusted - target_value)
        if best is None or diff < best_diff:
            best = it
            best_diff = diff

    # Accept candidate only if not absurdly far from target (e.g., within 4x)
    if best is not None:
        adjusted_best = best.price * mult
        if adjusted_best > target_value * 4 and target_value > 0:
            # too expensive relative to target
            return None
        return (best.id, best.price)
    return None


def craft_items(
    state,
    selections: List[Tuple[str, float]],
    mode: str,
    tier: int = 50,
) -> dict:
    """Perform crafting operation on selected items.

    - `selections`: list of (item_id, quality) tuples (qualities are per-instance)
    - `mode`: one of 'probabilistic', 'deterministic', 'fusion', 'upgrade'
    - `tier`: selected success tier (50,35,25,10). For deterministic/fusion tier is ignored.

    Returns a dict with keys: success(bool), cost(int), output: Optional[dict]
    """
    # compute average quality and adjusted sum
    qualities = [q for _, q in selections if q is not None]
    avg_q = float(sum(qualities) / len(qualities)) if qualities else 0.0
    adjusted_sum = compute_adjusted_sum(selections)

    # base cost: 0.2% of adjusted sum (0.002). Previously 1% — lowered per user request.
    cost = max(1, int(round(adjusted_sum * 0.002)))

    # Determine final multiplier and success chance depending on mode/tier
    if mode == "probabilistic":
        tier_info = TIERS.get(tier, TIERS[50])
        mult = tier_info["mult"]
        success_chance = tier / 100.0
    elif mode == "deterministic":
        mult = 1.0
        success_chance = 1.0
    elif mode == "fusion":
        # fusion: modest multiplier depending on count
        count = max(1, len(selections))
        mult = 1.0 + 0.05 * (count - 1)
        success_chance = 1.0
    elif mode == "upgrade":
        tier_info = TIERS.get(tier, TIERS[50])
        mult = 1.0
        success_chance = tier / 100.0
    else:
        mult = 1.0
        success_chance = 1.0

    target_value = adjusted_sum * mult

    # Choose category preservation: if all inputs same category -> preserve it
    categories = set()
    for iid, _ in selections:
        it = presets.ITEMS_BY_ID.get(iid)
        if it is not None:
            categories.add(it.category)
    preserved_category = categories.pop() if len(categories) == 1 else None

    # Simulate the attempt (random for probabilistic/upgrade modes)
    success = True
    if success_chance < 1.0:
        success = random.random() < success_chance

    # Generate new quality (always created anew; per-user requirement)
    new_q = generate_new_quality(avg_q, tier)

    # Select output template close to target_value; if none, create synthetic
    sel = select_output_template(target_value, new_q, category=preserved_category)
    output = None
    if sel is not None:
        out_id, out_price = sel
        out_template = presets.ITEMS_BY_ID.get(out_id)
        if out_template is not None:
            output = {
                "id": out_template.id,
                "name": out_template.name,
                "price": out_template.price,
                "category": out_template.category,
                "quality": new_q,
                "success": success,
                "expected_value": target_value,
            }
    else:
        # create a synthetic crafted item — compute base price so that price * mult(new_q) ~= target_value
        base_price = 0
        mult_q = price_multiplier(float(new_q))
        if mult_q > 0:
            base_price = int(round(target_value / mult_q))
        cid = f"crafted_{int(time.time() * 1000)}"
        cname = f"Crafted {'/'.join([presets.ITEMS_BY_ID[i].category for i, _ in selections]) if preserved_category else 'Weapon'}"
        output = {
            "id": cid,
            "name": cname,
            "price": base_price,
            "category": preserved_category or "weapon",
            "quality": new_q,
            "success": success,
            "expected_value": target_value,
        }

    return {"success": success, "cost": cost, "output": output, "avg_q": avg_q, "adjusted_sum": adjusted_sum}
