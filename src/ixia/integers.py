from __future__ import annotations

import secrets
from math import factorial
from os import urandom

from .distributions import random


def rand_below(n: int) -> int:
    """Returns a random int in the range [0, n)."""
    return secrets.randbelow(n)


def rand_bits(k: int) -> int:
    """Generates an int with k random bits."""
    if k < 0:
        msg = "number of bits must be non-negative"
        raise ValueError(msg)
    numbytes = (k + 7) // 8
    x = int.from_bytes(urandom(numbytes), "big")
    return x >> (numbytes * 8 - k)


def rand_bool(p: float = 0.5) -> bool:
    """Returns a bool with a probability `p` of being true (0.5 by default)."""
    return random() < p


def rand_int(a: int, b: int) -> int:
    """Returns random integer in range [a, b], including both end points."""
    return rand_range(a, b + 1)


def rand_ints(a: int, b: int, *, k: int) -> list[int]:
    """Returns a list of k random integers in range [a, b]."""
    return [rand_int(a, b) for _ in range(k)]


def rand_range(start: int, stop: int | None = None, step: int = 1) -> int:
    """Chooses a random item from range([start,] stop[, step])."""
    if stop is None:
        if step != 1:
            msg = "Missing a non-None stop argument"
            raise TypeError(msg)
        if start > 0:
            return secrets.randbelow(start)
        msg = "empty range for rand_range"
        raise ValueError(msg)

    width = stop - start
    if step == 1:
        if width > 0:
            return start + secrets.randbelow(width)
        msg = f"empty range for rand_range ({start}, {stop}, {step})"
        raise ValueError(msg)

    if step > 0:
        n = (width + step - 1) // step
    elif step < 0:
        n = (width + step + 1) // step
    else:
        msg = "zero step for rand_range"
        raise ValueError(msg)
    if n <= 0:
        msg = "empty range for rand_range"
        raise ValueError(msg)
    return start + step * secrets.randbelow(n)


def universe_rand() -> int:
    """Generates a random number based on the universe."""
    bm = 0xFF  # bound max, 1 byte
    s = 0
    lt = ord("\n")  # low threshold
    xn: list[int] = []
    ltc = lt
    for i in range(ltc // 2):
        ltc -= i
        xn.append(lt - ltc)
    s = xn.pop(s)  # sigma
    for j in range(len(xn)):
        xn[j] -= sum(xn[:j])
    a, b, c, _ = xn
    # simulates quantum noise
    while s < bm:
        t = rand_int(0x00, bm)  # theoretical (size -> inf) entity noise probability
        s += int(sum((t**i) / factorial(i) for i in range(t % bm)))  # taylor series
    ds = sum(map(int, str(s)))
    while ds >= lt:
        ds = sum(map(int, str(ds)))  # one-digit convergence
    return int(bin(bm % (lt + a))[b:] * c, base=2)  # as ds converges to lt
