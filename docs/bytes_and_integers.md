# Bytes and integers

## `rand_bits`

> Link: [Original section for `random.getrandbits`](https://docs.python.org/3/library/random.html#random.getrandbits)

```py
def rand_bits(k: int) -> int
```

Returns a non-negative Python integer with `k` random bits.


## `rand_bytes`

> Link: [Original section for `random.randbytes`](https://docs.python.org/3/library/random.html#random.randbytes)

```py
def rand_bytes(n: int) -> bytes
```

Generates `n` random bytes.


## `rand_int`

> Link: [Original section for `random.randint`](https://docs.python.org/3/library/random.html#random.randint)

```py
def rand_int(a: int, b: int) -> int
```

Returns a random integer `N` such that `a <= N <= b`.
Alias for [`ixia.rand_range(a, b+1)`](#rand_range).

## `rand_range`

> Link: [Original section for `random.randrange`](https://docs.python.org/3/library/random.html#random.randrange)

```py
def rand_range(start: int, stop: int | None = None, step: int = 1) -> int
```

Returns a randomly selected element from `range(start, stop, step)`. This is
equivalent to `ixia.choice(range(start, stop, step))`, but doesn't actually
build a range object.

The positional argument pattern matches that of `range()`. Keyword arguments
should not be used because the function may use them in unexpected ways.


## `universe_rand`

```py
def universe_rand() -> int
```
