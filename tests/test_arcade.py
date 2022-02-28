from io import StringIO

from hypothesis import given
from hypothesis import strategies as st

from arcade_cli import arcade
from custom_strats import star_strat


@given(st.lists(star_strat))
def test_save_load(orginal_stars):
    save_file = StringIO()

    arcade.store_stars_in_file(orginal_stars, save_file)
    save_file.seek(0)
    loaded_stars = arcade.load_stars_from_file(save_file)

    assert orginal_stars == loaded_stars
