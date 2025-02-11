from __future__ import annotations

import secrets
import string
from base64 import urlsafe_b64encode
from io import BufferedIOBase, TextIOBase
from os import PathLike, urandom
from pathlib import Path
from typing import overload

from .distributions import PASSPHRASE_DEFAULT_PATH, _Cache
from .sequences import choice, choices

ALNUM_CHARSET = string.ascii_letters + string.digits


def passphrase(
    n: int, *, sep: str = "-", words_path: PathLike[str] | str = PASSPHRASE_DEFAULT_PATH
) -> str:
    """Generate an XKCD-style passphrase."""
    if n < 1:
        return ""
    words_path = Path(words_path)
    if words_path == PASSPHRASE_DEFAULT_PATH and not words_path.exists():
        msg = "word list unavailable at the default path; please provide a valid path"
        raise NotImplementedError(msg)
    if not (_Cache.words and _Cache.words_path == words_path):
        _Cache.words = words_path.read_text().splitlines()
        _Cache.words_path = words_path
    return sep.join(choices(_Cache.words, k=n)).lower()


def rand_bytes(n: int = 32) -> bytes:
    """Generate `n` random bytes. Defaults to 32."""
    return urandom(n)


def rand_hex(n: int) -> str:
    """Return a hex string composed of `n` random bytes."""
    return "".join(f"{secrets.randbelow(255):02x}" for _ in range(n))


@overload
def rand_line(file: TextIOBase | PathLike[str] | str) -> str: ...


@overload
def rand_line(file: BufferedIOBase) -> bytes: ...


def rand_line(file: TextIOBase | BufferedIOBase | PathLike[str] | str) -> str | bytes:
    """
    Return a random line from a file. Given a string or a path-like object, assume it is
    a path, read it, and return a random line from the read content.
    Given a readable IO object, read it, and return a random line from the read content.
    Return a bytes object if provided an IO object in binary mode.
    """
    if isinstance(file, (TextIOBase, BufferedIOBase)):
        try:
            # Suppressing an error due to mypy using a different method of merging
            # types. Here, mypy sees a `Sequence[object]`, while pyright sees a
            # `str | bytes`. See this for more details:
            # https://microsoft.github.io/pyright/#/mypy-comparison?id=unions-vs-joins
            return choice(file.read().splitlines())  # type: ignore[return-value]
        except IndexError:
            msg = "no more data in file"
            raise EOFError(msg) from None
    with Path(file).open() as f:
        return rand_line(f)


def rand_urlsafe(n: int = 32) -> str:
    """Return a random URL-safe text string, in Base64 encoding."""
    return urlsafe_b64encode(rand_bytes(n)).rstrip(b"=").decode("ascii")


def rand_printable(n: int) -> str:
    """Return a random printable ASCII (32..126) string of length `n`."""
    return "".join(chr(secrets.randbelow(95) + 32) for _ in range(n))


def rand_alnum(n: int) -> str:
    """Return a random alphanumeric string of length `n`."""
    return "".join(choices(ALNUM_CHARSET, k=n))
