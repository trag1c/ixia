import math
import string
from io import StringIO
from pathlib import Path
from unittest.mock import patch

import pytest

from ixia import (
    passphrase,
    rand_alnum,
    rand_bytes,
    rand_hex,
    rand_line,
    rand_printable,
    rand_urlsafe,
)

URLSAFE_CHARSET = string.ascii_letters + string.digits + "_-"


def test_passphrase(tmp_path: Path) -> None:
    (path := tmp_path / "words.txt").write_text("one\ntwo\nthree\nfour\nfive")
    assert not passphrase(0, words_path=path)
    assert passphrase(1, words_path=path)


def test_passphrase_nonexistent() -> None:
    with patch("ixia.strings.Path") as path_mock:
        path_inst = path_mock.return_value
        path_inst.exists.return_value = False
        path_inst.__eq__.return_value = True
        with pytest.raises(NotImplementedError):
            passphrase(1)

        # Ignore the path entirely for n < 1
        assert not passphrase(0)


def test_bytes() -> None:
    with pytest.raises(ValueError, match="negative argument not allowed"):
        rand_bytes(-1)
    assert rand_bytes(0) == b""
    assert len(rand_bytes(8)) == 8
    assert len(rand_bytes()) == 32


def test_hex() -> None:
    for i in range(-50, 50):
        val = rand_hex(i)
        if i <= 0:
            assert not val
        else:
            assert len(val) == i * 2
            assert all(c in string.hexdigits for c in val)


def test_rand_line(tmp_path: Path) -> None:
    lines = ("hello", "there", "general", "kenobi")
    (path := tmp_path / "sample.txt").write_text("\n".join(lines))

    assert rand_line(path) in lines
    assert rand_line(str(path)) in lines

    with path.open() as f:
        assert rand_line(f) in lines

    with path.open("rb") as f:
        assert rand_line(f) not in lines  # type: ignore[comparison-overlap]


def test_rand_line_bin(tmp_path: Path) -> None:
    lines = (b"hello", b"there", b"general", b"kenobi")
    (path := tmp_path / "sample.bin").write_bytes(b"\n".join(lines))

    with path.open("rb") as f:
        assert rand_line(f) in lines

    with path.open() as f:
        assert rand_line(f) not in lines  # type: ignore[comparison-overlap]


def test_rand_line_empty(tmp_path: Path) -> None:
    (path := tmp_path / "empty.txt").touch()

    with pytest.raises(EOFError):
        rand_line(path)

    with pytest.raises(EOFError):
        rand_line(StringIO(""))

    buf = StringIO("hello\nthere")
    buf.readline()
    assert rand_line(buf) == "there"

    buf = StringIO("there")
    buf.readline()
    with pytest.raises(EOFError):
        rand_line(buf)


def test_urlsafe() -> None:
    for i in range(100):
        val = rand_urlsafe(i)
        assert all(c in URLSAFE_CHARSET for c in val)
        assert len(val) == math.ceil(4 / 3 * i)  # expected 33% overhead


def test_rand_printable() -> None:
    for i in range(1000):
        val = rand_printable(i)
        assert len(val) == i
        assert all(ord(c) in range(32, 127) for c in val)


def test_rand_alnum() -> None:
    for i in range(1000):
        val = rand_alnum(i)
        assert len(val) == i
        assert all(map(str.isalnum, val))
