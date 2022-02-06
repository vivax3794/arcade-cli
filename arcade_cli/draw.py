from __future__ import annotations

import math
from typing import TYPE_CHECKING

import cv2
from sklearn import cluster

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

    print(max_x, max_x * (1920 / 1080), max_y)

    # a / x = 1.78
    # a = 1.78*x

    if mode == "ratio":
        scale = max(max_x * (1920 / 1080), max_y)
        stars = [(x / scale / 1.78, y / scale, type_) for x, y, type_ in stars]
    else:
        stars = [(x / max_x, y / max_y, type_) for x, y, type_ in stars]

    return stars


def draw_formula(
    form: str,
    start: float,
    end: float,
    step: float,
    y_min: float | None,
    y_max: float | None,
    star_type: int,
) -> List[Star]:
    stars = []

    while start <= end:
        y = eval(form, {}, {"x": start, "math": math})
        if (y_min is None or y >= y_min) and (y_max is None or y <= y_max):
            stars.append((start, y, star_type))
        start += step

    return stars


# BY MATISSE: https://discord.com/channels/799761313772863508/803440400193814589/926572167951433829
def render_colors(image, scale):
    img = cv2.imread(image)
    print(img.shape)
    width = int(img.shape[1] / scale)
    height = int(img.shape[0] / scale)
    print(width)
    print(height)
    img = cv2.resize(img, (width, height))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    img = img.reshape((img.shape[1] * img.shape[0], 3))
    kmeans = cluster.KMeans(n_clusters=24)
    _ = kmeans.fit(img)

    labels = kmeans.labels_
    stars = []
    for y in range(height):
        for x in range(width):
            label = labels[y * width + x]
            stars.append((x, y, label + 1))

    return stars
