from hypothesis import strategies as st

from arcade_cli import arcade


star_cords = st.floats(allow_nan=False, allow_infinity=False, min_value=-(10**9), max_value=10**9)
star_strat = st.tuples(star_cords, star_cords, st.integers(min_value=0, max_value=25))
