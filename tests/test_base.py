from math import ceil
from string import ascii_letters, digits, hexdigits

from pytest import raises

from ixia import (
    rand_below,
    rand_bits,
    rand_bytes,
    rand_hex,
    rand_int,
    rand_range,
    rand_urlsafe,
    universe_rand,
)

URLSAFE_CHARSET = ascii_letters + digits + "_-"


def test_below():
    with raises(ValueError):
        rand_below(0)
    for i in range(1, 101):
        assert rand_below(i) in range(i)


def test_bits():
    with raises(ValueError):
        rand_bits(-1)
    for i in range(100):
        assert rand_bits(i).bit_length() <= i


def test_bytes():
    with raises(ValueError):
        rand_bytes(-1)
    assert rand_bytes(0) == b""
    assert len(rand_bytes(8)) == 8
    assert len(rand_bytes()) == 32


def test_hex():
    for i in range(-50, 50):
        val = rand_hex(i)
        if i <= 0:
            assert not val
        else:
            assert len(val) == i * 2
            assert all(c in hexdigits for c in val)


def test_int():
    for i in range(50):
        assert rand_int(i, i) == i
        assert rand_int(-i, i) in range(-i, i + 1)


def test_range():
    with raises(TypeError):
        rand_range(1, step=2)
    with raises(ValueError):
        rand_range(-1)
    with raises(ValueError):
        rand_range(50, 0)
    for i in range(1, 51):
        assert rand_range(-i, i) in range(-i, i)


def test_urlsafe():
    for i in range(100):
        val = rand_urlsafe(i)
        assert all(c in URLSAFE_CHARSET for c in val)
        assert len(val) == ceil(4 / 3 * i)  # expected 33% overhea


def test_universe_rand():
    for _ in range(1000):
        assert universe_rand() == 42
