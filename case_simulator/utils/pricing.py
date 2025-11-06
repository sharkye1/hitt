from __future__ import annotations


def price_multiplier(q: float) -> float:
    """Map quality q to a price multiplier according to configured tiers.

    Same algorithm used by case opening logic. Input q is expected in [0.0, 1.0).
    """
    # Safety clamp
    q = max(0.0, min(q, 0.999999))

    # Below 0.5: linear from 0.4 -> 0.65 at 0.5
    if q < 0.5:
        return 0.4 + (0.65 - 0.4) * (q / 0.5)

    # 0.5 .. 0.75: linear 0.65 -> 0.75
    if q < 0.75:
        return 0.65 + (0.75 - 0.65) * ((q - 0.5) / 0.25)

    # 0.75 .. 0.9: linear 0.75 -> 1.0
    if q < 0.9:
        return 0.75 + (1.0 - 0.75) * ((q - 0.75) / 0.15)

    # Anchors for >0.9 progression
    anchors = [
        (0.9, 1.0),
        (0.91, 1.05),
        (0.93, 1.30),
        (0.95, 1.70),
        (0.99, 3.00),
        (0.9950, 5.00),
    ]

    # between 0.9 and 0.995: linear interpolate between anchors
    for i in range(len(anchors) - 1):
        x0, m0 = anchors[i]
        x1, m1 = anchors[i + 1]
        if x0 <= q < x1:
            t = (q - x0) / (x1 - x0)
            return m0 + (m1 - m0) * t

    # 0.9950 < q <= 0.9989 -> fixed 8.0 (800%) according to spec
    if q <= 0.9989:
        if q > 0.9950:
            return 8.0

    # q >= 0.9990 -> progressive per-0.0001 increments starting at 10.0
    if q >= 0.9990:
        # number of steps of 0.0001 above 0.9990
        steps = (q - 0.9990) / 0.0001
        return 10.0 + steps

    # fallback: if q in small gap between 0.9989 and 0.9990, return 8.0
    return 8.0
