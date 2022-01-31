from __future__ import annotations

from typing import TYPE_CHECKING
import math

if TYPE_CHECKING:
    from typing import List

    from arcade_cli.arcade import Star


def normalize(stars: List[Star]) -> List[Star]:
    max_x = max(x for x, _, _ in stars)
    max_y = max(y for _, y, _ in stars)
    scale = max(max_x, max_y)

    min_x = min(x for x, _, _ in stars)
    min_y = min(y for _, y, _ in stars)

    return [
        (x / scale - min_x, y / scale - min_y, type_)
        for x, y, type_ in stars
    ]


def draw_formula(form: str, start: float, end: float, step: float, star_type: int) -> List[Star]:
    stars = []

    while start <= end:
        y = eval(form, {}, {"x": start, "math": math})
        stars.append((start, y, star_type))
        start += step
    
    return normalize(stars)