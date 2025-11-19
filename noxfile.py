import sys

import nox

ARTIFACTS = (
    'coverage.xml',
    'htmlcov',
    'doc/build',
    'build',
    'dist',
    '*.egg-info',
    '.coverage',
    '.mypy_cache',
    '.pytest_cache',
    '.hypothesis',
    '.ipynb_checkpoints',
    '.ruff_cache',
)

# Make `nox` default to running tests if you just do `nox`
nox.options.sessions = ['test']


def do_clean(session: nox.Session) -> None:
    for artifact in sorted(ARTIFACTS):
        session.run('rm', '-rf', artifact, external=True)


def do_performance(session: nox.Session) -> None:
    # keep -v to see warnings; no build isolation to match your invoke cmd
    session.run(
        sys.executable,
        'static_frame/performance/main.py',
        '--performance',
        '*',
        external=True,
    )


# default is unit tests, for full do:
# nox -s test -- --full
# To show warnings:
# nox -s test --warnings
def do_test(session: nox.Session) -> None:
    warnings = '--warnings' in session.posargs

    fps = []
    fps.append('test')
    w_flag = '--disable-pytest-warnings'
    cmd = f'pytest -s --tb=native {w_flag if warnings else ""} {" ".join(fps)}'

    session.run(
        *cmd.split(' '),
        external=True,
    )


def do_lint(session: nox.Session) -> None:
    session.run(
        'ruff',
        'check',
        external=True,
    )


def do_mypy(session: nox.Session) -> None:
    session.run(
        'mypy',
        '--strict',
        external=True,
    )


def do_format(session: nox.Session) -> None:
    for cmd in ('ruff check --select I --fix', 'ruff format'):
        session.run(
            *cmd.split(' '),
            external=True,
        )


def do_format_check(session: nox.Session) -> None:
    for cmd in ('ruff check --select I', 'ruff format --check'):
        session.run(
            *cmd.split(' '),
            external=True,
        )


# NOTE: use `nox -s test` to launch a session


@nox.session(python=False)  # use current environment
def clean(session):
    do_clean(session)


@nox.session(python=False)
def test(session):
    do_test(session)


@nox.session(python=False)
def lint(session):
    do_lint(session)


@nox.session(python=False)
def format(session):
    do_format(session)


@nox.session(python=False)
def mypy(session):
    do_mypy(session)


@nox.session(python=False)
def quality(session):
    do_lint(session)
    do_format_check(session)
    do_mypy(session)


@nox.session(python=False)  # use current environment
def build(session):
    do_clean(session)
    session.run(
        sys.executable,
        '-m',
        'pip',
        'install',
        'build',
        external=True,
    )
    session.run(
        sys.executable,
        '-m',
        'build',
        external=True,
    )
