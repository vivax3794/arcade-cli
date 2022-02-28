import os
import nox

os.environ.update({"PDM_IGNORE_SAVED_PYTHON": "1", "PDM_USE_VENV": "1"})

@nox.session(python=["3.8", "3.9", "3.10"], reuse_venv=True)
def tests(session):
    session.run("pdm", "install", "-G", "test", external=True)
    session.run("pytest", "tests")

@nox.session(python="3.8", reuse_venv=True)
def lint(session):
    session.run("pdm", "install", "-G", "lint", external=True)
    session.run("flake8", "arcade_cli")
    session.run("pyright", "arcade_cli")