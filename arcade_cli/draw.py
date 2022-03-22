from __future__ import annotations
from fileinput import filename

import math
import os
from io import BytesIO
from typing import TYPE_CHECKING, Any
import random
import string

# cv2 is strange with typing
# (I just hope it is not because of pdm it is acting strange.)
if TYPE_CHECKING:
    cv2: Any = ...
else:
    import cv2
import svgpathtools
from matplotlib import pyplot as plt
from sklearn import cluster

plt.switch_backend("svg")

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

    # a / x = 1.78
    # a = 1.78*x

    if mode == "ratio":
        scale = max(max_x / (1920 / 1080), max_y) or 1
        stars = [((x / scale) / (1920 / 1080), y / scale, type_) for x, y, type_ in stars]
    else:
        stars = [(x / (max_x or 1), y / (max_y or 1), type_) for x, y, type_ in stars]

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
        try:
            y = eval(form, {}, {"x": start, "math": math})
        except Exception as e:
            print(e)
        else:
            if (y_min is None or y >= y_min) and (y_max is None or y <= y_max):
                stars.append((start, y, star_type))
        start += step

    return stars


# BY MATISSE: https://discord.com/channels/799761313772863508/803440400193814589/926572167951433829
def render_colors(image: str, scale: int) -> List[Star]:
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

    labels: List[int] = kmeans.labels_  # type: ignore
    stars = []
    for y in range(height):
        for x in range(width):
            label = labels[y * width + x]
            stars.append((x, y, label + 1))

    return stars


def render_svg(filename: str, path_res: int) -> List[Star]:
    paths, _ = svgpathtools.svg2paths(filename)  # type: ignore

    stars = []
    for path in paths:
        for index in range(path_res):
            pos: complex = path.point(index / 200)  # type: ignore
            x = pos.real
            y = pos.imag
            stars.append((x, y, 1))
    return stars



def render_letter(text: str) -> List[Star]:
    fig = plt.figure(figsize=(0.01, 0.01))
    fig.text(0, 0, text)

    output = BytesIO()
    fig.savefig(output, dpi=300, format="svg")
    plt.close(fig)

    output.seek(0)
    svg_code = output.read().decode()

    # generate random filename that is very unlikely to be in use
    filename = "".join(random.choice(string.ascii_letters) for _ in range(20)) + ".svg"

    with open(filename, "w+") as f:
        f.write(svg_code)

    stars = render_svg(filename, 200)
    os.remove(filename)
    return stars

def render_text(text: str) -> List[Star]:
    text = text.replace(" ", "_") # make sure spaces actually work
    stars: List[Star] = [(0, 0, 0)]
    for letter in text:
        try:
            new_stars = render_letter(letter)
        except Exception as e:
            print("ERROR:", e)
            continue

        max_x = max(x for x, _, _ in stars)
        stars.extend((x + max_x, y, type_) for x, y, type_ in new_stars)

    max_y = max(y for _, y, _ in stars)

    return [(x, max_y - y, type_) for x, y, type_ in stars]
