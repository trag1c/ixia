# Ixia
Ixia is a cryptographically secure RNG library. It mainly merges `secrets`'
security with `random`'s versatility, but also adds some of its own
functions, such as [`ixia.passphrase()`](https://trag1c.github.io/ixia/sequences.html#ixiapassphrase), [`ixia.shuffled()`](https://trag1c.github.io/ixia/sequences.html#ixiashuffled) or
[`ixia.universe_rand()`](https://trag1c.github.io/ixia/bytes_and_integers.html#ixiauniverse_rand). All random values are generated using `urandom` (or `BCryptGenRandom` on Windows).

## Installation
Ixia is available on PyPI and can be installed with pip, or any other Python package manager:
```sh
$ pip install ixia
```
(Some systems may require you to use `pip3`, `python -m pip`, or `py -m pip` instead.)

## Documentation
Ixia documentation is available at https://trag1c.github.io/ixia/.

## License
Ixia is licensed under the MIT License.

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
