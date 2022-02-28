import os

import pytest
from hypothesis import given
from hypothesis import strategies as st

from arcade_cli import cli


def test_jwt_present(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ARCADE_JWT", "test test")

    assert cli.read_jwt() == "test test"


def test_jwt_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("ARCADE_JWT", raising=False)

    with pytest.raises(SystemExit):
        cli.read_jwt()
