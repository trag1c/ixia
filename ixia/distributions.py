from __future__ import annotations

from math import acos, cos, e, exp, fabs, floor, lgamma, log, log2, pi, sin, sqrt, tau
from operator import index
from os import urandom
from typing import ClassVar, Union

Number = Union[int, float]


class Cache:
    gauss_next: float | None = None
    words: ClassVar[list[str]] = []
    words_path: str = "/usr/share/dict/words"


def beta_variate(alpha: Number, beta: Number) -> float:
    """
    Beta distribution.

    Conditions on the parameters are alpha > 0 and beta > 0.
    Returned values range between 0 and 1.
    """
    # This version is due to Janne Sinkkonen, and matches all the std
    # texts (e.g., Knuth Vol 2 Ed 3 pg 134 "the beta distribution").
    if y := gamma_variate(alpha, 1.0):
        return y / (y + gamma_variate(beta, 1.0))
    return 0.0


def binomial_variate(n: int = 1, p: Number = 0.5) -> int:
    """
    Binomial random variable.

    Gives the number of successes for n independent trials
    with the probability of success in each trial being p:

        sum(random() < p for _ in range(n))

    Returns an integer in the range [0, n]
    """
    # Error checking and edge cases
    if n < 0:
        msg = "n must be non-negative"
        raise ValueError(msg)
    if p == 0.0:
        return 0
    if p == 1.0:
        return n
    if not (0.0 < p < 1.0):
        msg = "p must be in range [0, 1]"
        raise ValueError(msg)

    # Fast path for a common case
    if n == 1:
        return index(random() < p)

    # Exploit symmetry to establish:  p <= 0.5
    if p > 0.5:
        return n - binomial_variate(n, 1.0 - p)

    if n * p < 10.0:
        # BG: Geometric method by Devroye with running time of O(np).
        # https://dl.acm.org/doi/pdf/10.1145/42372.42381
        x = y = 0
        if not (c := log2(1.0 - p)):
            return x
        while True:
            y += floor(log2(random()) / c) + 1
            if y > n:
                return x
            x += 1

    # BTRS: Transformed rejection with squeeze method by Wolfgang Hörmann
    # https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.47.8407
    setup_complete = False
    alpha = m = h = lpq = 0.0

    spq = sqrt(n * p * (1.0 - p))  # Standard deviation of the distribution
    b = 1.15 + 2.53 * spq
    a = -0.0873 + 0.0248 * b + 0.01 * p
    c = n * p + 0.5
    vr = 0.92 - 4.2 / b

    while True:
        us = 0.5 - fabs(u := random() - 0.5)
        k = floor((2.0 * a / us + b) * u + c)
        if k < 0 or k > n:
            continue

        # The early-out "squeeze" test substantially reduces
        # the number of acceptance condition evaluations.
        v = random()
        if us >= 0.07 and v <= vr:
            return k

        # Acceptance-rejection test.
        # Note, the original paper errorneously omits the call to log(v)
        # when comparing to the log of the rescaled binomial distribution.
        if not setup_complete:
            alpha = (2.83 + 5.1 / b) * spq
            lpq = log(p / (1.0 - p))
            m = floor((n + 1) * p)
            h = lgamma(m + 1) + lgamma(n - m + 1)
            setup_complete = True
        v *= alpha / (a / (us * us) + b)
        if log(v) <= h - lgamma(k + 1) - lgamma(n - k + 1) + (k - m) * lpq:
            return k


def expo_variate(lambda_: float = 1.0) -> float:
    """
    Exponential distribution.

    lambda_ is 1.0 divided by the desired mean. It should be nonzero.
    Return values range from 0 to positive infinity if lambda_ is positive,
    and from negative infinity to 0 if lambda_ is negative.
    """
    # we use 1-random() instead of random() to preclude
    # the possibility of taking the log of zero
    return -log(1.0 - random()) / lambda_


def gamma_variate(alpha: Number, beta: Number) -> float:
    """
    Gamma distribution.

    Conditions on the parameters are alpha > 0 and beta > 0.
    """
    if alpha <= 0.0 or beta <= 0.0:
        msg = "gamma_variate: alpha and beta must be > 0.0"
        raise ValueError(msg)

    if alpha > 1.0:
        # Uses R.C.H. Cheng, "The generation of Gamma
        # variables with non-integral shape parameters",
        # Applied Statistics, (1977), 26, No. 1, p71-74

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
        # expovariate(1/beta)  # noqa: ERA001
        return -log(1.0 - random()) * beta

    # alpha is between 0 and 1 (exclusive)
    # Uses ALGORITHM GS of Statistical Computing - Kennedy & Gentle
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
    # Uses Kinderman and Monahan method. Reference: Kinderman,
    # A.J. and Monahan, J.F., "Computer generation of random
    # variables using the ratio of uniform deviates", ACM Trans
    # Math Software, 3, (1977), pp257-260.
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
    # Jain, pg. 495
    return (1.0 - random()) ** (-1.0 / alpha)  # type: ignore[no-any-return]


def random() -> float:
    """Generates a random number in range [0.0, 1.0)."""
    return (int.from_bytes(urandom(7), "big") >> 3) * 2**-53


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


def von_mises_variate(mu: Number, kappa: Number) -> float:
    """
    Circular data distribution.

    mu is the mean angle, expressed in raidans between 0 and tau, and kappa is the
    concentration parameter, which must be greater than or equal to zero. If kappa is
    equal to zero, this distribution reduces to a uniform random angle over
    the range 0 to tau.
    """
    # Based upon an algorithm published in: Fisher, N.I.,
    # "Statistical Analysis of Circular Data", Cambridge
    # University Press, 1993.

    # Thanks to Magnus Kessler for a correction to the
    # implementation of step 4.
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
    # Jain, pg. 499; bug fix courtesy Bill Arms
    return alpha * (-log(1.0 - random())) ** (1.0 / beta)  # type: ignore[no-any-return]
