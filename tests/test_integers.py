import re
from string import ascii_letters, digits

import pytest

from ixia import rand_bits, rand_bool, rand_int, rand_ints, rand_range, universe_rand

URLSAFE_CHARSET = ascii_letters + digits + "_-"


def test_bool() -> None:
    assert rand_bool(p=1.0) is True
    assert rand_bool(p=0.0) is False
    assert 200 < sum(rand_bool() for _ in range(1000)) < 800
    assert sum(rand_bool(p=0.9) for _ in range(1000)) > 500
    assert sum(rand_bool(p=0.01) for _ in range(1000)) < 100


def test_universe_rand() -> None:
    for _ in range(1000):
        assert universe_rand() == 42


def test_rand_bits() -> None:
    for bit_count in range(10):
        for _ in range(1000):
            assert rand_bits(bit_count) in range(2**bit_count)


def test_rand_bits_negative() -> None:
    with pytest.raises(
        ValueError, match=re.escape("number of bits must be non-negative")
    ):
        rand_bits(-1)


def test_rand_ints() -> None:
    assert not rand_ints(1, 0, k=0)
    for _ in range(1000):
        a, b, k = rand_int(1, 10), rand_int(11, 20), rand_int(1, 20)
        out = rand_ints(a, b, k=k)
        assert len(out) == k
        assert max(out) <= b
        assert min(out) >= a


def test_rand_range() -> None:
    for _ in range(1000):
        a, b = rand_int(-10, 10), rand_int(11, 30)
        assert rand_range(b) in range(b)
        assert rand_range(a, b) in range(a, b)

        step = 1 if rand_bool() else rand_int(2, 4)
        assert rand_range(a, b, step) in range(a, b, step)
        if step != 1:
            assert rand_range(b, a, -step) in range(b, a, -step)


def test_rand_range_erroneous_cases() -> None:
    with pytest.raises(TypeError, match=re.escape("missing a non-None stop argument")):
        rand_range(1, step=2)

    with pytest.raises(ValueError, match=re.escape("empty range for rand_range")):
        rand_range(-1)

    start, stop = 1, -1
    with pytest.raises(
        ValueError, match=re.escape(f"empty range for rand_range ({start}, {stop}, 1)")
    ):
        rand_range(start, stop)

    with pytest.raises(ValueError, match=re.escape("zero step for rand_range")):
        rand_range(1, 2, 0)

    with pytest.raises(ValueError, match=re.escape("empty range for rand_range")):
        rand_range(20, 10, 2)
