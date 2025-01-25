# Ixia
Ixia is a cryptographically secure Python RNG library. It mainly merges
`secrets`' security with `random`'s versatility, but also rolls some of its own
functions, such as [`ixia.passphrase()`](strings_and_bytes.md#ixiapassphrase),
[`ixia.shuffled()`](sequences.md#ixiashuffled) or
[`ixia.universe_rand()`](integers.md#ixiauniverse_rand). All random
values are generated using `urandom` (or `BCryptGenRandom` on Windows).

## ⚠️ Important Notes
While supporting Python 3.9+, Ixia is based on the Python 3.12 implementation
of the `random` module. The following changes have been made to the module
since Python 3.9:

- `gauss`, `expovariate` and `normalvariate` have default parameter values
- `binomialvariate` was added

Additionally, Ixia executes 3.9+ deprecations, thus:

- `ixia.rand_range` doesn't convert non-integer types to equivalent integers
- `ixia.sample` doesn't support `set` as a sequence type
- `ixia.shuffle` doesn't support the `random` parameter

## Credits
- The original `random` module documentation & implementation:
  [Python Software Foundation](https://docs.python.org/3/library/random.html)
- `universe_rand` implementation: [qexat](https://github.com/qexat)
