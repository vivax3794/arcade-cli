from hypothesis import given, example
from hypothesis import strategies as st
import pytest

from arcade_cli import draw
from custom_strats import star_strat


@given(st.lists(star_strat, min_size=1), st.sampled_from(["full", "ratio"]))
def test_normalize_range(stars, mode):
    new_stars = draw.normalize(stars, mode)

    xs = [x for x, _, _ in new_stars]
    ys = [y for _, y, _ in new_stars]

    assert min(xs) >= 0 and max(xs) <= 1.01, "x values not within 0-1 range"
    assert min(ys) >= 0 and max(ys) <= 1.01, "y values not within 0-1 range"


@given(st.lists(star_strat, min_size=1), st.sampled_from(["full", "ratio"]))
def test_normalize_left_corner(stars, mode):
    new_stars = draw.normalize(stars, mode)

    xs = [x for x, _, _ in new_stars]
    ys = [y for _, y, _ in new_stars]

    assert min(xs) == 0, "left x not equal to 0"
    assert min(ys) == 0, "top y not equal to 0"


@given(st.lists(star_strat, min_size=1))
def test_normalize_full(stars):
    new_stars = draw.normalize(stars, "full")

    xs = [x for x, _, _ in new_stars]
    ys = [y for _, y, _ in new_stars]

    assert max(xs) in {0, 1}, "x does not reache edge of the screen"
    assert max(ys) in {0, 1}, "y does not reache edge of the screen"



@given(st.lists(star_strat, min_size=1))
def test_normalize_ratio_edges(stars):
    new_stars = draw.normalize(stars, "ratio")

    xs = [x for x, _, _ in new_stars]
    ys = [y for _, y, _ in new_stars]

    assert pytest.approx(max(xs)) in (0, 1) or pytest.approx(max(ys)) in (0, 1), "both edges do not reache end of screen."

@given(st.lists(star_strat, min_size=1))
def test_normalize_ratio_keeps_ratio(stars):
    new_stars = draw.normalize(stars, "ratio")

    old_x = max(x for x, _, _ in stars) - min(x for x, _, _ in stars)
    old_y = max(y for _, y, _ in stars) - min(y for _, y, _ in stars)

    new_x = max(x for x, _, _ in new_stars) * (1920 / 1080)
    new_y = max(y for _, y, _ in new_stars)

    if old_y == 0 or new_y == 0:
        return

    assert pytest.approx(old_x/old_y) == new_x/new_y, "ratio not kept after normalizing"