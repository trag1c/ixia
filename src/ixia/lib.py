from __future__ import annotations

import secrets
from base64 import urlsafe_b64encode
from bisect import bisect
from collections.abc import Iterable, MutableSequence, Sequence
from io import TextIOBase
from itertools import accumulate
from math import acos, ceil, cos, e, exp, factorial, floor, isfinite, log, pi, sin, sqrt, tau
from os import urandom
from pathlib import Path
from sys import platform
from typing import Any, TypeVar, Union

Number = Union[int, float]
PASSPHRASE_DEFAULT_PATH = "/usr/share/dict/words"
PASSPHRASE_PLATFORMS = {"linux", "darwin", "aix"}
T = TypeVar("T")


class Cache:
    gauss_next: float | None = None
    words: list[str] = []
    words_path: str = "/usr/share/dict/words"


def beta_variate(alpha: Number, beta: Number) -> float:
    """
    Beta distribution.

    Conditions on the parameters are alpha > 0 and beta > 0.
    Returned values range between 0 and 1.
    """
    if y := gamma_variate(alpha, 1.0):
        return y / (y + gamma_variate(beta, 1.0))
    return 0.0


def choice(seq: Sequence[T]) -> T:
    """Chooses a random element from a non-empty sequence."""
    return secrets.choice(seq)


def choices(
    seq: Sequence[T],
    weights: Sequence[Number] | None = None,
    *,
    cumulative_weights: Sequence[Number] | None = None,
    k: int = 1,
) -> list[T]:
    """
    Returns a k sized list of sequence elements chosen with replacement.

    If the relative weights or cumulative weights are not specified,
    the selections are made with equal probability.
    """
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
        raise ValueError("The number of weights does not match the sequence")

    total = cumulative_weights[-1] + 0.0
    if total <= 0.0:
        raise ValueError("Total of weights must be greater than zero")

    if not isfinite(total):
        raise ValueError("Total of weights must be finite")

    hi = n - 1
    return [seq[bisect(cumulative_weights, random() * total, 0, hi)] for _ in range(k)]


def expo_variate(lambda_: float) -> float:
    """
    Exponential distribution.

    lambda_ is 1.0 divided by the desired mean. It should be nonzero.
    Return values range from 0 to positive infinity if lambda_ is positive,
    and from negative infinity to 0 if lambda_ is negative.
    """
    return -log(1.0 - random()) / lambda_


def gamma_variate(alpha: Number, beta: Number) -> float:
    """
    Gamma distribution.

    Conditions on the parameters are alpha > 0 and beta > 0.
    """
    if alpha <= 0.0 or beta <= 0.0:
        raise ValueError("gamma_variate: alpha and beta must be > 0.0")

    if alpha > 1.0:
        ainv = sqrt(2.0 * alpha - 1.0)
        b = alpha - log(4)
        c = alpha + ainv
        sg = 1.0 + log(4.5)

        while True:
            u = random()
            if not 1e-7 < u < 0.9999999:
                continue
            u2 = 1.0 - random()
            v = log(u / (1.0 - u)) / ainv
            x = alpha * exp(v)
            z = u * u * u2
            r = b + c * v - x
            if r + sg - 4.5 * z >= 0 or r >= log(z):
                return x * beta

    if alpha == 1.0:
        return -log(1.0 - random()) * beta

    while True:
        b = (e + alpha) / e
        p = b * random()
        x = p ** (1.0 / alpha) if p <= 1.0 else -log((b - p) / alpha)
        u = random()
        if p > 1.0:
            if u <= x ** (alpha - 1.0):
                break
        elif u <= exp(-x):
            break
    return x * beta


def gauss(mu: Number = 0.0, sigma: Number = 1.0) -> float:
    """
    Gaussian distribution.

    mu is the mean, and sigma is the standard deviation.
    This is slightly faster than the normal_variate() function.

    Not thread-safe without a lock around calls.
    """
    z = Cache.gauss_next
    Cache.gauss_next = None
    if z is None:
        xtau = random() * tau
        g2rad = sqrt(-2.0 * log(1.0 - random()))
        z = cos(xtau) * g2rad
        Cache.gauss_next = sin(xtau) * g2rad
    return mu + z * sigma


def log_norm_variate(mu: Number, sigma: Number) -> float:
    """
    Log normal distribution.

    If you take the natural logarithm of this distribution, you'll get
    a normal distribution with mean mu and standard deviation sigma.
    mu can have any value, and sigma must be greater than zero.
    """
    return exp(normal_variate(mu, sigma))


def normal_variate(mu: Number = 0.0, sigma: Number = 1.0) -> float:
    """
    Normal distribution.

    mu is the mean, and sigma is the standard deviation.
    """
    nv = 4 * exp(-0.5) / sqrt(2.0)
    while True:
        u1 = random()
        u2 = 1.0 - random()
        z = nv * (u1 - 0.5) / u2
        if z * z / 4.0 <= -log(u2):
            break
    return mu + z * sigma


def pareto_variate(alpha: Number) -> float:
    """
    Pareto distribution.

    alpha is the shape parameter.
    """
    return (1.0 - random()) ** (-1.0 / alpha)


def passphrase(
    n: int, *, sep: str = "-", words_path: str = PASSPHRASE_DEFAULT_PATH
) -> str:
    """Generates an XKCD-style passphrase."""
    if words_path == PASSPHRASE_DEFAULT_PATH and platform not in PASSPHRASE_PLATFORMS:
        raise NotImplementedError(f"word list unavailable on {platform}")
    if not Cache.words or Cache.words_path != words_path:
        Cache.words = Path(words_path).read_text().splitlines()
        Cache.words_path = words_path
    return sep.join(choices(Cache.words, k=n)).lower()


def rand_below(n: int) -> int:
    """Returns a random int in the range [0, n)."""
    return secrets.randbelow(n)


def rand_bits(k: int) -> int:
    """Generates an int with k random bits."""
    if k < 0:
        raise ValueError("number of bits must be non-negative")
    numbytes = (k + 7) // 8
    x = int.from_bytes(urandom(numbytes), "big")
    return x >> (numbytes * 8 - k)


def rand_bool() -> bool:
    """Returns a random bool."""
    return bool(round(random()))


def rand_bytes(n: int = 32) -> bytes:
    """Generates n random bytes. Defaults to 32."""
    return urandom(n)


def rand_hex(n: int) -> str:
    """Returns a hex string composed of n random bytes."""
    return "".join(f"{secrets.randbelow(255):02x}" for _ in range(n))


def rand_int(a: int, b: int) -> int:
    """Returns random integer in range [a, b], including both end points."""
    return rand_range(a, b + 1)


def rand_line(file: TextIOBase | str) -> str:
    """
    Returns a random line from a file. Given a string, assumes it is
    a path, reads it, and returns a random line from the read content.
    Given a readable IO object, reads it,
    and returns a random line from the read content.
    """
    if isinstance(file, TextIOBase):
        return choice(file.read().splitlines())
    with Path(file).open() as f:
        return rand_line(f)


def rand_range(start: int, stop: int | None = None, step: int = 1) -> int:
    """Chooses a random item from range([start,] stop[, step])."""
    if stop is None:
        if step != 1:
            raise TypeError("Missing a non-None stop argument")
        if start > 0:
            return secrets.randbelow(start)
        raise ValueError("empty range for rand_range")

    width = stop - start
    if step == 1:
        if width > 0:
            return start + secrets.randbelow(width)
        raise ValueError(f"empty range for rand_range ({start}, {stop}, {step})")

    if step > 0:
        n = (width + step - 1) // step
    elif step < 0:
        n = (width + step + 1) // step
    else:
        raise ValueError("zero step for rand_range")
    if n <= 0:
        raise ValueError("empty range for rand_range")
    return start + step * secrets.randbelow(n)


def rand_urlsafe(n: int = 32) -> str:
    """Returns a random URL-safe text string, in Base64 encoding."""
    return urlsafe_b64encode(rand_bytes(n)).rstrip(b"=").decode("ascii")


def random() -> float:
    """Generates a random number in range [0.0, 1.0)."""
    return (int.from_bytes(urandom(7), "big") >> 3) * 2**-53


def sample(seq: Sequence[T], k: int, *, counts: Iterable[int] | None = None) -> list[T]:
    """
    Chooses k unique random elements from the sequence.

    Returns a new list containing elements from the sequence while leaving the original
    sequence unchanged. The resulting list is in selection order so that all sub-slices
    will also be valid random samples. This allows raffle winners (the sample) to be
    partitioned into grand prize and second place winners (the subslices).

    Members of the sequence don't need to be hashable nor unique. If the sequence
    contains repeats, then each occurence is a possible selection in the sample.

    Repeated elements can be specified one at a time or with
    the optional counts parameter. For example:

        sample(["red", "blue"], counts=[4, 2], k=5)

    is equivalent to:

        sample("red", "red", "red", "red", "blue", "blue"], k=5)

    To choose a sample from a range of integers, use range() for the sequence
    argument. This is especially fast and space efficient
    for sampling from a large sequence:

        sample(range(10_000_000), 60)
    """
    n = len(seq)

    if counts is not None:
        cum_counts = list(accumulate(counts))
        if len(cum_counts) != n:
            raise ValueError("The number of counts does not match the sequence")
        total = cum_counts.pop()
        if not isinstance(total, int):
            raise TypeError("Counts must be integers")
        if total <= 0:
            raise ValueError("Total of counts must be greater than zero")
        selections = sample(range(total), k=k)
        return [seq[bisect(cum_counts, s)] for s in selections]
    if not 0 <= k <= n:
        raise ValueError("Sample larger than sequence or is negative")

    result: list[T] = []
    setsize = 21
    if k > 5:
        setsize += 4 ** ceil(log(k * 3, 4))

    if n <= setsize:
        pool = list(seq)
        for i in range(k):
            j = secrets.randbelow(n - i)
            result.append(pool[j])
            pool[j] = pool[n - i - 1]
    else:
        selected: set[int] = set()
        for _ in range(k):
            while (j := secrets.randbelow(n)) in selected:
                pass
            selected.add(j)
            result.append(seq[j])

    return result


def shuffle(seq: MutableSequence[Any]) -> None:
    """
    Shuffles the sequence in place, and returns None.

    Use shuffled() for out of place shuffling.
    """
    for i in range(len(seq) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        seq[i], seq[j] = seq[j], seq[i]


def shuffled(seq: Sequence[T]) -> MutableSequence[T]:
    """
    Returns a shuffled copy of the sequence.
    Returns a list for immutable sequences.

    Use shuffle() for in place shuffling.
    """
    if isinstance(seq, MutableSequence):
        seq_ = seq[:]
        shuffle(seq_)
        return seq_
    return sample(seq, len(seq))


def triangular(low: float = 0.0, high: float = 1.0, mode: float | None = None) -> float:
    """
    Triangular distribution.

    Continuous distribution bounded by given lower and upper limits,
    and having a given mode value in-between.
    """
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
    """Generates a random number in range [a, b) or [a, b] depending on rounding."""
    return a + (b - a) * random()


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


def von_mises_variate(mu: Number, kappa: Number) -> float:
    """
    Circular data distribution.

    mu is the mean angle, expressed in raidans between 0 and tau, and kappa is the
    concentration parameter, which must be greater than or equal to zero. If kappa is
    equal to zero, this distribution reduces to a uniform random angle over
    the range 0 to tau.
    """
    if kappa <= 1e-6:
        return tau * random()

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
        return (mu + acos(f)) % tau
    return (mu - acos(f)) % tau


def weibull_variate(alpha: Number, beta: Number) -> float:
    """
    Weibull distribution.

    alpha is the scale parameter, beta is the shape parameter.
    """
    return alpha * (-log(1.0 - random())) ** (1.0 / beta)
