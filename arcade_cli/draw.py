from __future__ import annotations

import math
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import List

    from arcade_cli.arcade import Star


def normalize(stars: List[Star], mode: str) -> List[Star]:
    # sourcery skip: lift-return-into-if, remove-unnecessary-else, swap-if-else-branches
    min_x = min(x for x, _, _ in stars)
    min_y = min(y for _, y, _ in stars)
    stars = [(x - min_x, y - min_y, type_) for x, y, type_ in stars]

    max_x = max(x for x, _, _ in stars)
    max_y = max(y for _, y, _ in stars)

    if mode == "keep":
        scale = max(max_x, max_y)
        stars = [(x / scale, y / scale, type_) for x, y, type_ in stars]
    else:
        stars = [(x / max_x, y / max_y, type_) for x, y, type_ in stars]

    return stars


def draw_formula(
    form: str, start: float, end: float, step: float, star_type: int
) -> List[Star]:
    stars = []

    while start <= end:
        y = eval(form, {}, {"x": start, "math": math})
        stars.append((start, y, star_type))
        start += step

    return stars
