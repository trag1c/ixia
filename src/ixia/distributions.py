from __future__ import annotations

from math import acos, cos, e, exp, log, pi, sin, sqrt, tau
from os import urandom
from typing import Union

Number = Union[int, float]


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


def expo_variate(lambda_: float = 1.0) -> float:
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
