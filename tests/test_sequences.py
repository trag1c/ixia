import re
from enum import Enum
from io import StringIO
from pathlib import Path
from typing import Any
from unittest.mock import patch

import pytest

from ixia import (
    beta_variate,
    choice,
    choices,
    passphrase,
    perm,
    rand_enum,
    rand_line,
    sample,
    shuffled,
)

TEST_LIST = [6, 3, 9, 1, 2, 4, 8, 0, 5, 7]
TEST_TUPLE = tuple(TEST_LIST)


def test_shuffled() -> None:
    for _ in range(300):
        a = shuffled(TEST_LIST)
        b = shuffled(TEST_TUPLE)
        assert sorted(a) == sorted(b) == sorted(TEST_LIST)


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


def test_choice() -> None:
    for _ in range(100):
        assert choice(range(1000)) in range(1000)


def test_choice_empty_seq() -> None:
    with pytest.raises(
        IndexError, match=re.escape("cannot choose from an empty sequence")
    ):
        choice([])


def test_choice_with_weights() -> None:
    assert choice([1, 2], weights=[0, 1]) == 2


@pytest.mark.parametrize(
    ("args", "kwargs", "exc_type", "exc_msg"),
    [
        (
            ([1], 1),
            {},
            TypeError,
            "the number of choices must be a keyword argument: k=1",
        ),
        (([1], 1.0), {}, TypeError, "'float' object is not iterable"),
        (
            ([1], [1]),
            {"cumulative_weights": [1]},
            TypeError,
            "cannot specify both weights and cumulative weights",
        ),
        (
            ([1],),
            {"cumulative_weights": [1, 2]},
            ValueError,
            "the number of weights does not match the sequence",
        ),
        (([0], [0]), {}, ValueError, "total of weights must be greater than zero"),
        (([0], [1e309]), {}, ValueError, "total of weights must be finite"),
    ],
)
def test_choices_erroneous_cases(
    args: tuple[Any, ...],
    kwargs: dict[str, Any],
    exc_type: type[BaseException],
    exc_msg: str,
) -> None:
    with pytest.raises(exc_type, match=re.escape(exc_msg)):
        choices(*args, **kwargs)


def test_sample() -> None:
    base = range(21, 37)
    for k in range(17):
        s = sample(base, k)
        assert len(s) == k
        assert set(s) <= set(base)


def test_sample_counts() -> None:
    for _ in range(100):
        assert sample([1, 2], 1, counts=[1, 0]) == [1]
        assert sample([1, 2], 1, counts=[1, 10**10]) == [2]
        assert sample([1, 2], 50, counts=[0, 50]) == [2] * 50
        assert sample([1, 2], 500, counts=[0, 50000]) == [2] * 500


@pytest.mark.parametrize(
    ("args", "kwargs", "exc_type", "exc_msg"),
    [
        (([1], 2), {}, ValueError, "sample larger than sequence or is negative"),
        (([1], -1), {}, ValueError, "sample larger than sequence or is negative"),
        (
            ([1], 1),
            {"counts": [1, 2]},
            ValueError,
            "the number of counts does not match the sequence",
        ),
        (([1, 2], 1), {"counts": "12"}, TypeError, "counts must be integers"),
        (
            ([1], 1),
            {"counts": [0]},
            ValueError,
            "total of counts must be greater than zero",
        ),
    ],
)
def test_sample_erroneous_cases(
    args: tuple[Any, ...],
    kwargs: dict[str, Any],
    exc_type: type[BaseException],
    exc_msg: str,
) -> None:
    with pytest.raises(exc_type, match=re.escape(exc_msg)):
        sample(*args, **kwargs)


def test_rand_enum() -> None:
    class Foo(Enum):
        A = 1
        B = 2
        C = 3

    for _ in range(100):
        assert isinstance(rand_enum(Foo), Foo)

    class Empty(Enum):
        pass

    with pytest.raises(ValueError, match=re.escape("enum has 0 members")):
        rand_enum(Empty)


def test_perm() -> None:
    for _ in range(500):
        size = round(beta_variate(1, 8) * 5000)
        p = perm(size)
        assert len(p) == size
        assert set(p) == set(range(size))
