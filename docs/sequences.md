# Functions for sequences

## `choice`

> Link: [Original section for `random.choices`](https://docs.python.org/3/library/random.html#random.choice)

```py
def choice(seq: Sequence[T]) -> T
```

Chooses a random element from a non-empty sequence `seq`.

If `seq` is empty, `IndexError` is raised.


## `choices`

> Link: [Original section for `random.choices`](https://docs.python.org/3/library/random.html#random.choices)

```py
def choices(
    seq: Sequence[T],
    weights: Sequence[Number] | None = None,
    *,
    cumulative_weights: Sequence[Number] | None = None,
    k: int = 1,
) -> list[T]
```

Returns a k sized list of elements chosen from the sequence `seq` with
replacement. If the sequence is empty, `IndexError` is raised.

If a `weights` sequence is specified, selections are made according to the
relative weights. Alternatively, if a `cumulative_weights` sequence is given,
the selections are made according to the cumulative weights (perhaps computed
using `itertools.accumulate()`). For example, the relative weights
`[10, 5, 30, 5]` are equivalent to the cumulative weights `[10, 15, 45, 50]`.
Internally, the relative weights are converted to cumulative weights before
making selections, so supplying the cumulative weights saves work.

If neither `weights` nor `cumulative_weights` are specified, selections are
made with equal probability. If a weights sequence is supplied, it must be the
same length as the `seq` sequence. Specifying both `weights` and
`cumulative_weights` will raise a `TypeError`.

The `weights` or `cumulative_weights` can use any numeric type that
interoperates with the `float` values returned by `ixia.random()` (that
includes integers, floats, and fractions but excludes dceimals). Weights are
assumed to be non-negative and finite. If all weights are zero, a `ValueError` is raised.

## `sample`

```py
def sample(
    seq: Sequence[T],
    k: int,
    *,
    counts: Iterable[int] | None = None
) -> list[T]
```

## `shuffle`

```py
def shuffle(seq: MutableSequence[Any]) -> None
```


## `shuffled`

```py
def shuffled(seq: Sequence[T]) -> MutableSequence[T]
```
