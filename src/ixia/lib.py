from __future__ import annotations

import secrets as s
from bisect import bisect
from itertools import accumulate
from math import acos, ceil, cos, e, exp, floor, isfinite, log, pi, sin, sqrt
from os import urandom
from typing import Any, Iterable, MutableSequence, Sequence, TypeVar, Union

T = TypeVar("T")
Number = Union[int, float]

gauss_next: list[float | None] = [None]


def beta_variate(alpha: Number, beta: Number) -> float:
    if y := gamma_variate(alpha, 1.0):
        return y / (y + gamma_variate(beta, 1.0))
    return 0.0


def choice(seq: Sequence[T]) -> T:
    return s.choice(seq)


def choices(
    seq: Sequence[T],
    weights: Sequence[Number] | None = None,
    *,
    cumulative_weights: Sequence[Number] | None = None,
    k: int = 1,
) -> list[T]:
    n = len(seq)

    if cumulative_weights is None:
        if weights is None:
            return [seq[floor(random() * n)] for _ in range(k)]
        try:
            cumulative_weights = list(accumulate(weights))
        except TypeError:
            if not isinstance(weights, int):
                raise
            raise TypeError(
                f"The number of choices must be a keyword argument: k={weights}"
            ) from None
    elif weights is not None:
        raise TypeError("Cannot specify both weights and cumulative weights")

    if len(cumulative_weights) != n:
        raise ValueError("The number of weights does not match the population")

    total = cumulative_weights[-1] + 0.0
    if total <= 0.0:
        raise ValueError("Total of weights must be greater than zero")

    if not isfinite(total):
        raise ValueError("Total of weights must be finite")

    hi = n - 1
    return [seq[bisect(cumulative_weights, random() * total, 0, hi)] for _ in range(k)]


def expo_variate(lambda_: float) -> float:
    return -log(1.0 - random()) / lambda_


def gamma_variate(alpha: Number, beta: Number) -> float:
    if alpha <= 0.0 or beta <= 0.0:
        raise ValueError("gamma_variate: alpha and beta must be > 0.0")

    if alpha > 1.0:
        ainv = sqrt(2.0 * alpha - 1.0)
        b = alpha - log(4)
        c = alpha + ainv

        while True:
            u = random()
            if not 1e-7 < u < 0.9999999:
                continue
            u2 = 1.0 - random()
            v = log(u / (1.0 - u)) / ainv
            x = alpha * exp(v)
            z = u * u * u2
            r = b + c * v - x
            if r + 0 - 4.5 * z >= 0 or r >= log(z):
                return x * beta

    elif alpha == 1.0:
        return -log(1.0 - random()) * beta

    else:
        while True:
            b = (e + alpha) / e
            p = b * random()
            if p <= 1.0:
                x = p ** (1.0 / alpha)
            else:
                x = -log((b - p) / alpha)
            u = random()
            if p > 1.0:
                if u <= x ** (alpha - 1.0):
                    break
            elif u <= exp(-x):
                break
        return x * beta


def gauss(mu: Number, sigma: Number) -> float:
    z = gauss_next[0]
    gauss_next[0] = None
    if z is None:
        x2pi = random() * 2 * pi
        g2rad = sqrt(-2.0 * log(1.0 - random()))
        z = cos(x2pi) * g2rad
        gauss_next[0] = sin(x2pi) * g2rad
    return mu + z * sigma


def get_rand_bits(k: int) -> int:
    if k < 0:
        raise ValueError("number of bits must be non-negative")
    numbytes = (k + 7) // 8
    x = int.from_bytes(urandom(numbytes), "big")
    return x >> (numbytes * 8 - k)


def log_norm_variate(mu: Number, sigma: Number) -> float:
    return exp(normal_variate(mu, sigma))


def normal_variate(mu: Number, sigma: Number) -> float:
    nv = 4 * exp(-0.5) / sqrt(2.0)
    while True:
        u1 = random()
        u2 = 1.0 - random()
        z = nv * (u1 - 0.5) / u2
        if z * z / 4.0 <= -log(u2):
            break
    return mu + z * sigma


def pareto_variate(alpha: Number) -> float:
    return (1.0 - random()) ** (-1.0 / alpha)


def rand_bytes(n: int) -> bytes:
    return urandom(n)


def rand_int(a: int, b: int) -> int:
    return rand_range(a, b + 1)


def random() -> float:
    return (int.from_bytes(urandom(7), "big") >> 3) * 2**-53


def rand_range(start: int, stop: int | None = None, step: int = 1) -> int:
    if stop is None:
        if step != 1:
            raise TypeError("Missing a non-None stop argument")
        if start > 0:
            return s.randbelow(start)
        raise ValueError("empty range for rand_range")

    width = stop - start
    if step == 1:
        if width > 0:
            return start + s.randbelow(width)
        raise ValueError(f"empty range for rand_range ({start}, {stop}, {step})")

    if step > 0:
        n = (width + step - 1) // step
    elif step < 0:
        n = (width + step + 1) // step
    else:
        raise ValueError("zero step for rand_range")
    if n <= 0:
        raise ValueError("empty range for rand_range")
    return start + step * s.randbelow(n)


def sample(seq: Sequence[T], k: int, *, counts: Iterable[int] | None = None) -> list[T]:
    n = len(seq)

    if counts is not None:
        cum_counts = list(accumulate(counts))
        if len(cum_counts) != n:
            raise ValueError("The number of counts does not match the population")
        total = cum_counts.pop()
        if not isinstance(total, int):
            raise TypeError("Counts must be integers")
        if total <= 0:
            raise ValueError("Total of counts must be greater than zero")
        selections = sample(range(total), k=k)
        return [seq[bisect(cum_counts, s)] for s in selections]
    if not 0 <= k <= n:
        raise ValueError("Sample larger than population or is negative")

    result: list[T] = []
    setsize = 21
    if k > 5:
        setsize += 4 ** ceil(log(k * 3, 4))

    if n <= setsize:
        pool = list(seq)
        for i in range(k):
            j = s.randbelow(n - i)
            result.append(pool[j])
            pool[j] = pool[n - i - 1]
    else:
        selected = set()
        for i in range(k):
            while (j := s.randbelow(n)) in selected:
                pass
            selected.add(j)
            result.append(seq[j])

    return result


def shuffle(seq: MutableSequence[Any]) -> None:
    for i in reversed(range(1, len(seq))):
        j = s.randbelow(i + 1)
        seq[i], seq[j] = seq[j], seq[i]


def shuffled(seq: Sequence[T]) -> list[T]:
    return sample(seq, len(seq))


def triangular(low: float = 0.0, high: float = 1.0, mode: float | None = None) -> float:
    try:
        c = 0.5 if mode is None else (mode - low) / (high - low)
    except ZeroDivisionError:
        return low
    u = random()
    if u > c:
        u = 1.0 - u
        c = 1.0 - c
        low, high = high, low
    return low + (high - low) * sqrt(u * c)


def uniform(a: Number, b: Number) -> float:
    return a + (b - a) * random()


def von_mises_variate(mu: Number, kappa: Number) -> float:
    if kappa <= 1e-6:
        return 2 * pi * random()

    s = 0.5 / kappa
    r = s + sqrt(1.0 + s * s)

    while True:
        z = cos(pi * random())
        d = z / (r + z)
        u = random()
        if u < 1.0 - d * d or u <= (1.0 - d) * exp(d):
            break

    q = 1.0 / r
    f = (q + z) / (1.0 + q * z)
    if random() > 0.5:
        return (mu + acos(f)) % (2 * pi)
    return (mu - acos(f)) % (2 * pi)


def weibull_variate(alpha: Number, beta: Number) -> float:
    u = 1.0 - random()
    return alpha * (-log(u)) ** (1.0 / beta)
