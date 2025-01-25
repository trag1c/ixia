# Integers

## `ixia.rand_below`

> **Link:** [Original section for `secrets.randbelow`](https://docs.python.org/3/library/secrets.html#secrets.randbelow)

```py
def rand_below(n: int) -> int
```

Returns a random int in the range $[0, n)$.


## `ixia.rand_bits`

> **Link:** [Original section for `random.getrandbits`](https://docs.python.org/3/library/random.html#random.getrandbits)

```py
def rand_bits(k: int) -> int
```

Returns a non-negative Python integer with `k` random bits.


## `ixia.rand_bool`

```py
def rand_bool() -> bool
```

Returns a random bool.


## `ixia.rand_int`

> **Link:** [Original section for `random.randint`](https://docs.python.org/3/library/random.html#random.randint)

```py
def rand_int(a: int, b: int) -> int
```

Returns a random integer `N` in the range $[a, b]$.
Alias for [`ixia.rand_range(a, b+1)`](#ixiarand_range).


## `ixia.rand_ints`

```py
def rand_ints(a: int, b: int, *, k: int) -> list[int]
```

Returns a list of `k` random integrs in the range $[a, b]$.  
Equivalent to `[rand_int(a, b) for _ in range(k)]`.


## `ixia.rand_range`

> **Link:** [Original section for `random.randrange`](https://docs.python.org/3/library/random.html#random.randrange)

```py
def rand_range(start: int, stop: int | None = None, step: int = 1) -> int
```

Returns a randomly selected element from `range(start, stop, step)`. This is
equivalent to `ixia.choice(range(start, stop, step))`, but doesn't actually
build a range object.

The positional argument pattern matches that of `range()`. Keyword arguments
should not be used because the function may use them in unexpected ways.


## `ixia.universe_rand`

```py
def universe_rand() -> int
```

Generates a random number based on the universe.

Thanks to the work of the recent Nobel Prize laureates, it was possible to code this function that computes a random number by simulating universe dimensions phasing on gamma ray emission using the sum of the spins of the pair positron/electron in a normalized Higgs field. Surprisingly, Taylor series is involved in this beautiful mathematical operation. It may or may not always return 42, we do not know.