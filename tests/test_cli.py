import re
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from pathlib import Path
from unittest.mock import patch

import pytest

from ixia import __main__ as main


@contextmanager
def patch_argv(*argv: str) -> Iterator[None]:
    with patch("sys.argv", ["ixia", *argv]):
        yield


@pytest.mark.parametrize("opt", ["-c", "--choice"])
def test_explicit_choice(opt: str, capsys: pytest.CaptureFixture[str]) -> None:
    options = ("a", "b", "c")

    with patch_argv(opt, *options):
        main.main()

    assert capsys.readouterr().out.strip() in options


@pytest.mark.parametrize("opt", ["-i", "--int", "--integer"])
@pytest.mark.parametrize("n", [1, 100, 1000])
def test_explicit_integer(opt: str, n: int, capsys: pytest.CaptureFixture[str]) -> None:
    with patch_argv(opt, str(n)):
        main.main()
    assert 1 <= int(capsys.readouterr().out) <= n


@pytest.mark.parametrize("opt", ["-f", "--float"])
@pytest.mark.parametrize("n", [1.0, 100.0, 1000.0])
def test_explicit_float(opt: str, n: float, capsys: pytest.CaptureFixture[str]) -> None:
    with patch_argv(opt, str(n)):
        main.main()

    assert 0.0 <= float(capsys.readouterr().out) <= n


@pytest.mark.parametrize("opt", ["-l", "--line"])
def test_explicit_line(
    opt: str, capsys: pytest.CaptureFixture[str], tmp_path: Path
) -> None:
    lines = ("foo", "bar", "baz")
    (path := tmp_path / "test.txt").write_text("\n".join(lines))

    with patch_argv(opt, str(path)):
        main.main()
    assert capsys.readouterr().out.strip() in lines


MISSING_ARG_REGEX = re.compile(
    r"error: argument (-\w)/.*: expected(?: at least)? one argument"
)


@pytest.mark.parametrize("opt", ["-c", "-i", "-f", "-l"])
def test_missing_arg(opt: str, capsys: pytest.CaptureFixture[str]) -> None:
    with patch_argv(opt), pytest.raises(SystemExit):
        main.main()
    out, err = capsys.readouterr()
    assert not out

    match = MISSING_ARG_REGEX.search(err)
    assert match
    assert match[1] == opt


@pytest.mark.parametrize(
    ("opt", "expected_err"),
    [
        ("-i", "invalid int value"),
        ("-f", "invalid float value"),
        ("-l", "No such file or directory"),
    ],
)
def test_incorrect_arg(
    opt: str, expected_err: str, capsys: pytest.CaptureFixture[str]
) -> None:
    with patch_argv(opt, "a"), pytest.raises(SystemExit):
        main.main()
    out, err = capsys.readouterr()
    assert not out
    assert expected_err in err


@pytest.mark.parametrize(
    ("value", "validator"),
    [
        ("3", lambda v: isinstance(v, int) and v in range(1, 4)),
        ("2.0", lambda v: isinstance(v, float) and 0.0 <= v <= 2.0),
        ("foo bar", lambda v: v in ("foo", "bar")),
    ],
)
def test_resolution_common(value: str, validator: Callable[[object], bool]) -> None:
    resolved = main._resolve_value(value)
    assert validator(resolved)


def test_resolution_file(tmp_path: Path) -> None:
    lines = ("foo", "bar", "baz")
    (path := tmp_path / "test.txt").write_text("\n".join(lines))
    assert main._resolve_value(str(path)) in lines


def test_multiple_arg_fail(capsys: pytest.CaptureFixture[str]) -> None:
    with patch_argv("-i", "1", "-f", "2.0"), pytest.raises(SystemExit):
        main.main()
    out, err = capsys.readouterr()
    assert not out
    assert "not allowed with argument" in err


def test_resolution_triggered(capsys: pytest.CaptureFixture[str]) -> None:
    with patch_argv(options := "foo bar baz"):
        main.main()
    assert capsys.readouterr().out.strip() in options.split()


def test_help_triggered(capsys: pytest.CaptureFixture[str]) -> None:
    with patch_argv():
        main.main()
    out, err = capsys.readouterr()
    assert not err
    assert out.startswith("usage: ixia")
