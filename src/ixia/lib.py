from __future__ import annotations
from math import acos, cos, exp, log, pi, sin, sqrt
from os import urandom
import secrets as s
from typing import Any, MutableSequence, Sequence, TypeVar, Union

T = TypeVar("T")
Number = Union[int, float]

gauss_next: list[float | None] = [None]


def betavariate(alpha, beta):
    ...


def choice(seq: Sequence[T]) -> T:
    return s.choice(seq)


def choices(population, weights=None, *, cum_weights=None, k=1):
    ...


def expovariate(lambda_: float) -> float:
    return -log(1.0 - random()) / lambda_


def gammavariate(alpha, beta):
    ...


def gauss(mu: Number, sigma: Number) -> float:
    z = gauss_next[0]
    gauss_next[0] = None
    if z is None:
        x2pi = random() * 2 * pi
        g2rad = sqrt(-2.0 * log(1.0 - random()))
        z = cos(x2pi) * g2rad
        gauss_next[0] = sin(x2pi) * g2rad
    return mu + z * sigma


def getrandbits(k):
    ...


def lognormvariate(mu: Number, sigma: Number) -> float:
    return exp(normalvariate(mu, sigma))


def normalvariate(mu: Number, sigma: Number) -> float:
    nv = 4 * exp(-0.5) / sqrt(2.0)
    while True:
        u1 = random()
        u2 = 1.0 - random()
        z = nv * (u1 - 0.5) / u2
        if z * z / 4.0 <= -log(u2):
            break
    return mu + z * sigma


def paretovariate(alpha: Number) -> float:
    u = 1.0 - random()
    return u ** (-1.0 / alpha)


def randbytes(n):
    ...


def randint(a: int, b: int) -> int:
    return randrange(a, b+1)


def random() -> float:
    return (int.from_bytes(urandom(7), "big") >> 3) * 2 ** -53


def randrange(start: int, stop: int | None = None, step: int = 1) -> int:
    if stop is None:
        if step != 1:
            raise TypeError("Missing a non-None stop argument")
        if start > 0:
            return s.randbelow(start)
        raise ValueError("empty range for randrange")

    width = stop - start
    if step == 1:
        if width > 0:
            return start + s.randbelow(width)
        raise ValueError(f"empty range for randrange ({start}, {stop}, {step})")

    if step > 0:
        n = (width + step - 1) // step
    elif step < 0:
        n = (width + step + 1) // step
    else:
        raise ValueError("zero step for randrange")
    if n <= 0:
        raise ValueError("empty range for randrange")
    return start + step * s.randbelow(n)


def sample(seq: Sequence[T], k: int, *, counts=None) -> Sequence[T]:
    ...


def shuffle(seq: MutableSequence[Any]) -> None:
    for i in reversed(range(1, len(seq))):
        j = s.randbelow(i + 1)
        seq[i], seq[j] = seq[j], seq[i]


def shuffled(seq: Sequence[T]) -> Sequence[T]:
    return sample(seq, len(seq))


def triangular(low: float = 0.0, high: float = 1.0, mode: float | None = None) -> float:
    u = random()
    try:
        c = 0.5 if mode is None else (mode - low) / (high - low)
    except ZeroDivisionError:
        return low
    if u > c:
        u = 1.0 - u
        c = 1.0 - c
        low, high = high, low
    return low + (high - low) * sqrt(u * c)


def uniform(a: Number, b: Number) -> float:
    return a + (b - a) * random()


def vonmisevariate(mu: Number, kappa: Number) -> float:
    if kappa <= 1e-6:
        return 2 * pi * random()

    s = 0.5 / kappa
    r = s + sqrt(1.0 + s * s)

    while True:
        u1 = random()
        z = cos(pi * u1)
        d = z / (r + z)
        u2 = random()
        if u2 < 1.0 - d * d or u2 <= (1.0 - d) * exp(d):
            break

    q = 1.0 / r
    f = (q + z) / (1.0 + q * z)
    u3 = random()
    if u3 > 0.5:
        return (mu + acos(f)) % (2 * pi)
    return (mu - acos(f)) % (2 * pi)


def weibullvariate(alpha: Number, beta: Number) -> float:
    u = 1.0 - random()
    return alpha * (-log(u)) ** (1.0 / beta)
