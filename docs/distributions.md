# Real-valued distributions

## `ixia.beta_variate`

> **Link:** [Original section for `random.betavariate`](https://docs.python.org/3/library/random.html#random.betavariate)

```py
def beta_variate(alpha: Number, beta: Number) -> float
```

Beta distribution.

Conditions on the parameters are `alpha > 0` and `beta > 0`.
Returned values range between $0$ and $1$.


## `ixia.expo_variate`

> **Link:** [Original section for `random.expovariate`](https://docs.python.org/3/library/random.html#random.expovariate)

```py
def expo_variate(lambda_: float = 1.0) -> float
```

Exponential distribution.

`lambda_` is $1$ divided by the desired mean. It should be nonzero.
Returned values are in range $[0, +\infty)$ for `lambda_ > 0`,
and $(-\infty, 0]$ for `lambda_ < 0`.


## `ixia.gamma_variate`

> **Link:** [Original section for `random.gammavariate`](https://docs.python.org/3/library/random.html#random.gammavariate)

```py
def gamma_variate(alpha: Number, beta: Number) -> float
```

Gamma distribution.

Conditions on the parameters are `alpha > 0` and `beta > 0`.

The probability distribution function is
$$f(x)=\frac{x^{\alpha-1}\cdot e^{\frac{-x}{\beta}}}{\Gamma(\alpha)\cdot\beta^\alpha}$$

## `ixia.gauss`

> **Link:** [Original section for `random.gauss`](https://docs.python.org/3/library/random.html#random.gauss)

```py
def gauss(mu: Number, sigma: Number) -> float
```

Normal distribution, also called the Gaussian distribution.

`mu` is the mean, and `sigma` is the standard deviation. This is slightly
faster than the [`ixia.normal_variate()`](#normal_variate) function.

> **Multithreading Note**  
> When two threads call this function simultaneously, it is possible that they
> will receive the same return value.
> This can be avoided in two ways:
> 1. Put locks around all calls
> 2. Use the slower, but thread-safe [`ixia.normal_variate()`](#normal_variate)
> function instead.


## `ixia.log_norm_variate`

> **Link:** [Original section for `random.lognormvariate`](https://docs.python.org/3/library/random.html#random.lognormvariate)

```py
def log_norm_variate(mu: Number, sigma: Number) -> float
```

Log normal distribution.

If you take the natural logarithm of this distribution, you'll get a normal
distribution with mean `mu` and standard deviation `sigma`. `mu` can have any
value, and `sigma` must be greater than $0$.


## `ixia.normal_variate`

> **Link:** [Original section for `random.normalvariate`](https://docs.python.org/3/library/random.html#random.normalvariate)

```py
def normal_variate(mu: Number, sigma: Number) -> float
```

Normal distribution.

`mu` is the mean, and `sigma` is the standard deviation.


## `ixia.pareto_variate`

> **Link:** [Original section for `random.paretovariate`](https://docs.python.org/3/library/random.html#random.paretovariate)

```py
def pareto_variate(alpha: Number) -> float
```

Pareto distribution.

`alpha` is the shape parameter.


## `ixia.random`

> **Link:** [Original section for `random.random`](https://docs.python.org/3/library/random.html#random.random)

```py
def random() -> float
```

Generates a random floating point number in the range $[0, 1)$.


## `ixia.triangular`

> **Link:** [Original section for `random.triangular`](https://docs.python.org/3/library/random.html#random.triangular)

```py
def triangular(
    low: float = 0.0,
    high: float = 1.0,
    mode: float | None = None
) -> float
```

Returns a random floating point number `N` such that `low <= N <= high` and
with the specified mode between those bounds. The low and high bounds default
to zero and one. The mode argument defaults to the midpoint between the
bounds, giving a symmetric distribution.


## `ixia.uniform`

> **Link:** [Original section for `random.uniform`](https://docs.python.org/3/library/random.html#random.uniform)

```py
def uniform(a: Number, b: Number) -> float
```

Returns a random floating point number `N` such that `a <= N <= b` for `a <= b`
and `b <= N <= a` for `b < a`.

The end-point value b may or may not be included in the range depending on
floating-point rounding in the equation `a + (b-a) * random()`.


## `ixia.von_mises_variate`

> **Link:** [Original section for `random.vonmisesvariate`](https://docs.python.org/3/library/random.html#random.vonmisesvariate)

```py
def von_mises_variate(mu: Number, kappa: Number) -> float
```

`mu` is the mean angle, expressed in radians between $0$
and $\tau$, and `kappa` is the concentration parameter, which must be
greater than or equal to zero. If `kappa` is equal to zero, this distribution
reduces to a uniform random angle over the range $0$ to $\tau$.


## `ixia.weibull_variate`

> **Link:** [Original section for `random.weibullvariate`](https://docs.python.org/3/library/random.html#random.weibullvariate)

```py
def weibull_variate(alpha: Number, beta: Number) -> float
```

Weibull distribution.

`alpha` is the scale parameter and `beta` is the shape parameter.
