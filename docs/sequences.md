# Sequences

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
includes integers, floats, and fractions but excludes decimals). Weights are
assumed to be non-negative and finite. If all weights are zero, a `ValueError` is raised.

## `sample`

> Link: [Original section for `random.sample`](https://docs.python.org/3/library/random.html#random.sample)

```py
def sample(
    seq: Sequence[T],
    k: int,
    *,
    counts: Iterable[int] | None = None
) -> list[T]
```

Returns a `k` length list of unique elements chosen from the sequence `seq`,
while keeping the original sequence unchanged. Used for random sampling without
replacement.

The resulting list is in selection order so that all sub-slices will also be
valid random samples. This allows raffle winners (the sample) to be partitioned
into grand prize and second place winners (the subslices).

Members of the sequence don't need to be hashable nor unique. If the sequence
contains repeats, then each occurrence is a possible selection in the sample.

Repeated elements can be specified one at a time or with the optional
keyword-only `counts` parameter. For example,
```py
sample(["red", "blue"], counts=[4, 2], k=5)
```
is equivalent to
```py
sample(["red", "red", "red", "red", "blue", "blue", k=5])
```
To choose a sample from a range of integers, use a `range()` object as an argument. This is especially fast and space efficient for sampling from a large population:
```py
sample(range(10_000_000), k=60)
```

If the sample size is larger than the population size, a `ValueError` is raised.

## `shuffle`

> Link: [Original section for `random.shuffle`](https://docs.python.org/3/library/random.html#random.shuffle)

```py
def shuffle(seq: MutableSequence[Any]) -> None
```

Shuffles the sequence `seq` in place.

> For out of place shuffling, use `ixia.shuffled()`.


## `shuffled`

```py
def shuffled(seq: Sequence[T]) -> MutableSequence[T]
```

Shuffles the sequence `seq` out of place.

If `seq` is a mutable type `M[T]`, the function will return `M[T]`.  
If `seq` is an immutable type `IM[T]`, the function will return `list[T]`.

> For in place shuffling, use `ixia.shuffle()`.