from __future__ import annotations

import math
import re
from collections import Counter
from typing import TYPE_CHECKING

import pytest

from ixia import (
    beta_variate,
    binomial_variate,
    expo_variate,
    gamma_variate,
    gauss,
    log_norm_variate,
    normal_variate,
    pareto_variate,
    random,
    triangular,
    uniform,
    von_mises_variate,
    weibull_variate,
)

if TYPE_CHECKING:
    from collections.abc import Callable


def test_beta_variate() -> None:
    for _ in range(10_000):
        alpha = uniform(1e-309, 10)
        beta = uniform(1e-309, 10)
        assert 0 <= beta_variate(alpha, beta) <= 1
        assert beta_variate(1e-309, alpha) == 0.0


@pytest.mark.parametrize(("alpha", "beta"), [(0, 1), (1, 0), (0, 0)])
def test_beta_variate_nonpositive_inputs(alpha: float, beta: float) -> None:
    with pytest.raises(
        ValueError, match=re.escape("gamma_variate: alpha and beta must be > 0.0")
    ):
        beta_variate(alpha, beta)


@pytest.mark.parametrize(
    ("n", "p", "possible_outcomes"),
    [
        (0, 0.5, {0}),
        (10, 0.0, {0}),
        (10, 1.0, {10}),
        (1, 0.3, {0, 1}),
        (1, 0.9, {0, 1}),
        (1, 0.0, {0}),
        (1, 1.0, {1}),
        (5, 1e-18, {0}),
        (5, 0.25, set(range(6))),
        (5, 0.75, set(range(6))),
        (100, 0.25, set(range(101))),
        (100, 0.75, set(range(101))),
        (10000, 0.75, set(range(10001))),
    ],
)
def test_binomial_variate(n: int, p: float, possible_outcomes: set[int]) -> None:
    for _ in range(10_000):
        assert binomial_variate(n, p) in possible_outcomes


@pytest.mark.parametrize(
    ("args", "exc_msg"),
    [
        ((-1,), "n must be non-negative"),
        ((1, -0.5), "p must be in range [0, 1]"),
        ((1, 1.5), "p must be in range [0, 1]"),
    ],
)
def test_binomial_variate_erroneous_cases(
    args: tuple[float, ...], exc_msg: str
) -> None:
    with pytest.raises(ValueError, match=re.escape(exc_msg)):
        binomial_variate(*args)


def test_expo_variate() -> None:
    for _ in range(100):
        assert expo_variate(1e309) == 0.0
        assert expo_variate(2.0) >= 0
        assert expo_variate(-2.0) <= 0

    res = [expo_variate(10.0) for _ in range(10)]
    assert len(res) == len(set(res))

    lambda_ = 2.0
    sample_mean = sum(expo_variate(lambda_) for _ in range(100_000)) / 1e5
    expected_mean = 1 / lambda_
    assert math.isclose(sample_mean, expected_mean, rel_tol=0.05)

    with pytest.raises(ZeroDivisionError):
        expo_variate(0.0)


def test_gamma_variate() -> None:
    for _ in range(10_000):
        alpha = uniform(1e-309, 10)
        beta = uniform(1e-309, 10)
        assert gamma_variate(alpha, beta) >= 0
        assert gamma_variate(1e-309, alpha) == 0.0


@pytest.mark.parametrize(("alpha", "beta"), [(0, 1), (1, 0), (0, 0)])
def test_gamma_variate_nonpositive_inputs(alpha: float, beta: float) -> None:
    with pytest.raises(
        ValueError, match=re.escape("gamma_variate: alpha and beta must be > 0.0")
    ):
        gamma_variate(alpha, beta)


def test_gauss_sigma_zero() -> None:
    for _ in range(1000):
        assert gauss(mu := random(), 0) == mu


@pytest.mark.parametrize(("mu", "sigma"), [(0, 1), (1, 1), (5, 2), (21, 37), (-19, 84)])
def test_gauss(mu: float, sigma: float) -> None:
    for _ in range(1000):
        assert mu - 8 * sigma <= gauss() <= mu + 8 * sigma


def test_log_norm_variate() -> None:
    for _ in range(1000):
        assert log_norm_variate(0, 1) > 0
        assert log_norm_variate(11, 0) == math.exp(11)


def test_normal_variate() -> None:
    for _ in range(1000):
        assert 980 < normal_variate(1000, 1) < 1020
        assert normal_variate(31, 0) == 31


@pytest.mark.parametrize(
    ("alpha", "min_threshold", "max_threshold"),
    [
        (2.0, 1.001, 100),
        (0.1, 1.001, 1e24),
        (-0.1, 1e-24, 0.999),
        (1e3, 1.000001, 1.005),
        (-1e3, 0.999, 0.9999),
    ],
)
def test_pareto_variate(
    alpha: float, min_threshold: float, max_threshold: float
) -> None:
    for _ in range(3):
        max_, min_ = -1e309, 1e309
        for _ in range(100_000):
            v = pareto_variate(alpha)
            max_ = max(max_, v)
            min_ = min(min_, v)
        assert min_ < min_threshold
        assert max_ > max_threshold


def test_pareto_variate_zero_fail() -> None:
    with pytest.raises(ZeroDivisionError):
        pareto_variate(0.0)


def test_random() -> None:
    for _ in range(100_000):
        assert 0.0 <= random() < 1.0


def test_triangular() -> None:
    for mode in (0.5, None):
        for _ in range(10000):
            assert 0 <= triangular(0, 1) <= 1

    for i in range(3):
        assert triangular(i, i, i) == i


@pytest.mark.parametrize(
    ("mode", "meets_criteria"),
    [
        (0.5, lambda mean: math.isclose(0.5, mean, rel_tol=0.01)),
        (0.25, lambda mean: mean < 0.5),
        (0.75, lambda mean: mean > 0.5),
    ],
)
def test_triangular_skews(mode: float, meets_criteria: Callable[[float], bool]) -> None:
    for _ in range(5):
        mean = sum(triangular(0, 1, mode) for _ in range(100_000)) / 1e5
        assert meets_criteria(mean)


def test_uniform() -> None:
    a, b = -10, 15
    for _ in range(1000):
        assert a <= uniform(a, b) <= b
        assert uniform(a, a) == a


@pytest.mark.parametrize(("mu", "kappa"), [(0, 0), (0, 1), (math.pi, 2), (math.pi, 5)])
def test_von_mises_variate(mu: float, kappa: float) -> None:
    for _ in range(1000):
        assert 0 <= von_mises_variate(mu, kappa) <= math.tau


def test_weibull_variate() -> None:
    for _ in range(1000):
        assert weibull_variate(0, 1) == 0
        assert weibull_variate(1, 1e309) == 1
        assert weibull_variate(1, 1e-309) in {0, 1e309}
        assert 0 < weibull_variate(2, 5) < 4
