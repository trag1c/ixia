from math import ceil
from string import ascii_letters, digits, hexdigits

from pytest import raises

from ixia import (
    rand_bytes,
    rand_hex,
    rand_urlsafe,
    random,
    universe_rand,
)

URLSAFE_CHARSET = ascii_letters + digits + "_-"


def test_bytes() -> None:
    with raises(ValueError):
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
            assert all(c in hexdigits for c in val)


def test_random() -> None:
    for _ in range(1000):
        assert 0 <= random() < 1


def test_urlsafe() -> None:
    for i in range(100):
        val = rand_urlsafe(i)
        assert all(c in URLSAFE_CHARSET for c in val)
        assert len(val) == ceil(4 / 3 * i)  # expected 33% overhead


def test_universe_rand() -> None:
    for _ in range(1000):
        assert universe_rand() == 42
