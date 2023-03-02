# Bytes, integers and strings

## `ixia.passphrase`

```py
def passphrase(
    n: int, *, sep: str = "-", words_path: str = "/usr/share/dict/words"
) -> str
```

Generates an [XKCD-style](https://xkcd.com/936/) passphrase made up from `n` words (based on the file specified by `words_path`), separated by `sep` (`-` by default).

⚠️ The default word list is not available on Windows.


## `ixia.rand_below`

> **Link:** [Original section for `secrets.randbelow`](https://docs.python.org/3/library/secrets.html#secrets.randbelow)

```py
def rand_below(n: int) -> int
```

Returns a random int in the range \\( [0, n) \\).


## `ixia.rand_bits`

> **Link:** [Original section for `random.getrandbits`](https://docs.python.org/3/library/random.html#random.getrandbits)

```py
def rand_bits(k: int) -> int
```

Returns a non-negative Python integer with `k` random bits.


## `ixia.rand_bytes`

> **Link:** [Original section for `random.randbytes`](https://docs.python.org/3/library/random.html#random.randbytes)

```py
def rand_bytes(n: int = 32) -> bytes
```

Generates `n` random bytes. Defaults to 32.


## `ixia.rand_hex`

> **Link:** [Original section for `secrets.token_hex`](https://docs.python.org/3/library/secrets.html#secrets.token_hex)

```py
def rand_hex(n: int) -> str
```

Returns a hex string composed of `n` random bytes.


## `ixia.rand_int`

> **Link:** [Original section for `random.randint`](https://docs.python.org/3/library/random.html#random.randint)

```py
def rand_int(a: int, b: int) -> int
```

Returns a random integer `N` such that `a <= N <= b`.
Alias for [`ixia.rand_range(a, b+1)`](#rand_range).

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


## `ixia.rand_urlsafe`

> [Original section for `secrets.token_urlsafe`](https://docs.python.org/3/library/secrets.html#secrets.token_urlsafe)

```py
def rand_urlsafe(n: int = 32) -> str
```

Returns a random URL-safe text string, composed of `n` bytes, in Base64 encoding. Defaults to 32.


## `ixia.universe_rand`

```py
def universe_rand() -> int
```

Generates a random number based on the universe.

Thanks to the work of the recent Nobel Prize laureates, it was possible to code this function that computes a random number by simulating universe dimensions phasing on gamma ray emission using the sum of the spins of the pair positron/electron in a normalized Higgs field. Surprisingly, Taylor series is involved in this beautiful mathematical operation. It may or may not always return 42, we do not know.