# Strings and bytes

## `ixia.passphrase`

```py
def passphrase(
    n: int, *, sep: str = "-", words_path: str = "/usr/share/dict/words"
) -> str
```

Generates an [XKCD-style](https://xkcd.com/936/) passphrase made up from `n` words (based on the file specified by `words_path`), separated by `sep` (`-` by default).

⚠️ The default word list is not available on Windows.


## `ixia.rand_alnum`

```py
def rand_alnum(n: int) -> str
```

Returns a random alphanumeric (A–Z, a–z, 0–9) string of length `n`.


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


## `ixia.rand_line`

```py
def rand_line(file: TextIOBase | str) -> str
```
Returns a random line from a file. Given a string, assumes it is
a path, reads it, and returns a random line from the read content.
Given a readable IO object, reads it,
and returns a random line from the read content.


## `ixia.rand_printable`

```py
def rand_printable(n: int) -> str
```

Returns a random printable ASCII (range 32–126) string of length `n`.


## `ixia.rand_urlsafe`

> [Original section for `secrets.token_urlsafe`](https://docs.python.org/3/library/secrets.html#secrets.token_urlsafe)

```py
def rand_urlsafe(n: int = 32) -> str
```

Returns a random URL-safe text string, composed of `n` bytes, in Base64 encoding. Defaults to 32.
