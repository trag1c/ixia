from __future__ import annotations

import secrets
from bisect import bisect
from collections.abc import Iterable, MutableSequence, Sequence
from itertools import accumulate
from math import ceil, floor, isfinite, log
from typing import Any, TypeVar

from .distributions import random

T = TypeVar("T")


def choice(
    seq: Sequence[T],
    weights: Sequence[float] | None = None,
    *,
    cumulative_weights: Sequence[float] | None = None,
) -> T:
    """
    Chooses a random element from a non-empty sequence.

    If the relative weights or cumulative weights are not specified,
    the selections are made with equal probability.
    """
    if not seq:
        msg = "cannot choose from an empty sequence"
        raise IndexError(msg)
    if weights is None and cumulative_weights is None:
        return secrets.choice(seq)
    return choices(seq, weights, cumulative_weights=cumulative_weights)[0]


def choices(
    seq: Sequence[T],
    weights: Sequence[float] | None = None,
    *,
    cumulative_weights: Sequence[float] | None = None,
    k: int = 1,
) -> list[T]:
    """
    Returns a k sized list of sequence elements chosen with replacement.

    If the relative weights or cumulative weights are not specified,
    the selections are made with equal probability.
    """
    n = len(seq)

    if cumulative_weights is None:
        if weights is None:
            n_ = n + 0.0  # convert to float for a small speed improvement
            return [seq[floor(random() * n_)] for _ in range(k)]
        try:
            cumulative_weights = list(accumulate(weights))
        except TypeError:
            if not isinstance(weights, int):
                raise
            msg = f"the number of choices must be a keyword argument: k={weights}"
            raise TypeError(msg) from None
    elif weights is not None:
        msg = "cannot specify both weights and cumulative weights"
        raise TypeError(msg)

    if len(cumulative_weights) != n:
        msg = "the number of weights does not match the sequence"
        raise ValueError(msg)

    total = cumulative_weights[-1] + 0.0  # convert to float
    if total <= 0.0:
        msg = "total of weights must be greater than zero"
        raise ValueError(msg)

    if not isfinite(total):
        msg = "total of weights must be finite"
        raise ValueError(msg)

    hi = n - 1
    return [seq[bisect(cumulative_weights, random() * total, 0, hi)] for _ in range(k)]


def sample(seq: Sequence[T], k: int, *, counts: Iterable[int] | None = None) -> list[T]:
    """
    Chooses k unique random elements from the sequence.

    Returns a new list containing elements from the sequence while leaving the original
    sequence unchanged. The resulting list is in selection order so that all sub-slices
    will also be valid random samples. This allows raffle winners (the sample) to be
    partitioned into grand prize and second place winners (the subslices).

    Members of the sequence don't need to be hashable nor unique. If the sequence
    contains repeats, then each occurrence is a possible selection in the sample.

    Repeated elements can be specified one at a time or with
    the optional counts parameter. For example:

        sample(["red", "blue"], counts=[4, 2], k=5)

    is equivalent to:

        sample(["red", "red", "red", "red", "blue", "blue"], k=5)

    To choose a sample from a range of integers, use range() for the sequence
    argument. This is especially fast and space efficient
    for sampling from a large sequence:

        sample(range(10_000_000), 60)
    """
    n = len(seq)

    if counts is not None:
        cum_counts = list(accumulate(counts))
        if len(cum_counts) != n:
            msg = "the number of counts does not match the sequence"
            raise ValueError(msg)
        total = cum_counts.pop()
        if not isinstance(total, int):
            msg = "counts must be integers"
            raise TypeError(msg)
        if total <= 0:
            msg = "total of counts must be greater than zero"
            raise ValueError(msg)
        selections = sample(range(total), k=k)
        return [seq[bisect(cum_counts, s)] for s in selections]
    if not 0 <= k <= n:
        msg = "sample larger than sequence or is negative"
        raise ValueError(msg)

    result: list[T] = []
    setsize = 21  # size of a small set minus size of an empty list
    if k > 5:
        setsize += 4 ** ceil(log(k * 3, 4))

    if n <= setsize:
        # An n-length list is smaller than a k-length set.
        # Invariant:  non-selected at pool[0 : n-i]
        pool = list(seq)
        for i in range(k):
            j = secrets.randbelow(n - i)
            result.append(pool[j])
            pool[j] = pool[n - i - 1]
    else:
        selected: set[int] = set()
        for _ in range(k):
            while (j := secrets.randbelow(n)) in selected:
                pass
            selected.add(j)
            result.append(seq[j])

    return result


def shuffle(seq: MutableSequence[Any]) -> None:
    """
    Shuffles the sequence in place, and returns None.

    Use shuffled() for out of place shuffling.
    """
    for i in range(len(seq) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        seq[i], seq[j] = seq[j], seq[i]


def shuffled(seq: Sequence[T]) -> MutableSequence[T]:
    """
    Returns a shuffled copy of the sequence.
    Returns a list for immutable sequences.

    Use shuffle() for in place shuffling.
    """
    if isinstance(seq, MutableSequence):
        seq_ = seq[:]
        shuffle(seq_)
        return seq_
    return sample(seq, len(seq))
