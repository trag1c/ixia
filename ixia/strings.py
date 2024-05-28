from __future__ import annotations

import secrets
from base64 import urlsafe_b64encode
from io import TextIOBase
from os import PathLike, urandom
from pathlib import Path

from .distributions import PASSPHRASE_DEFAULT_PATH, _Cache
from .sequences import choice, choices


def passphrase(
    n: int, *, sep: str = "-", words_path: PathLike[str] | str = PASSPHRASE_DEFAULT_PATH
) -> str:
    """Generates an XKCD-style passphrase."""
    words_path = Path(words_path)
    if words_path == PASSPHRASE_DEFAULT_PATH and not words_path.exists():
        msg = "word list unavailable at the default path; please provide a valid path"
        raise NotImplementedError(msg)
    if not (_Cache.words and _Cache.words_path == words_path):
        _Cache.words = words_path.read_text().splitlines()
        _Cache.words_path = words_path
    return sep.join(choices(_Cache.words, k=n)).lower()


def rand_bytes(n: int = 32) -> bytes:
    """Generates n random bytes. Defaults to 32."""
    return urandom(n)


def rand_hex(n: int) -> str:
    """Returns a hex string composed of n random bytes."""
    return "".join(f"{secrets.randbelow(255):02x}" for _ in range(n))


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


def rand_urlsafe(n: int = 32) -> str:
    """Returns a random URL-safe text string, in Base64 encoding."""
    return urlsafe_b64encode(rand_bytes(n)).rstrip(b"=").decode("ascii")
