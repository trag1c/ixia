# Ixia
Ixia is a cryptographically secure RNG library. It mainly merges `secrets`'
security with `random`'s versatility, but also adds some of its own
functions, such as [`ixia.passphrase()`](sequences.md#ixiapassphrase), [`ixia.shuffled()`](sequences.md#ixiashuffled) or
[`ixia.universe_rand()`](bytes_and_integers.md#ixiauniverse_rand). All random values are generated using `urandom` (or `BCryptGenRandom` on Windows).

## ⚠️ Important Notes
While supporting Python 3.8+, Ixia is based on the Python 3.11 implementation
of the `random` module. The following changes have been made to the module
since Python 3.8:
- `getrandbits` accepts 0 for `k`
- `choices` raises a `ValueError` if all weights are zero
- `sample` has a new `counts` parameter
- `gauss` and `normal_variate` have default parameter values

Additionally, Ixia executes 3.9+ deprecations, thus:
- `ixia.rand_range` doesn't convert non-integer types to equivalent integers
- `ixia.sample` doesn't support `set` as a sequence type
- `ixia.shuffle` doesn't support the `random` parameter

On the following pages of this documentation, function signatures often mention
the `Number` type—that's simply an alias to `Union[int, float]`.
