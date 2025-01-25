# Ixia
Ixia is a cryptographically secure Python RNG library. It mainly merges
`secrets`' security with `random`'s versatility, but also rolls some of its own
functions, such as [`ixia.passphrase()`][ixia-passphrase],
[`ixia.shuffled()`][ixia-shuffled],
or [`ixia.universe_rand()`][ixia-universe-rand].
All random values are generated using `urandom` (or `BCryptGenRandom` on Windows).

## Installation
Ixia is available on PyPI and can be installed with pip, or any other Python package manager:
```sh
$ pip install ixia
```
(Some systems may require you to use `pip3`, `python -m pip`, or `py -m pip` instead.)

## Documentation
Ixia documentation is available at https://trag1c.github.io/ixia/.

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

## Contributing

Contributions are welcome!

Please open an issue before submitting a pull request
(doesn't apply to minor changes like typos).

To get started:

1. Clone your fork of the project.
2. Install the project with [uv]:
```sh
uv sync
```
3. After you're done, use the following [`just`][just] recipes to check your
   changes (or run the commands manually):
```sh
just check     # pytest, mypy, ruff
just coverage  # pytest (with coverage), interrogate (docstring coverage)
```

## License
`ixia` is licensed under the [MIT License].  
© [trag1c], 2022–2024

[MIT License]: https://opensource.org/license/mit/
[trag1c]: https://github.com/trag1c/
[ixia-passphrase]: https://trag1c.github.io/ixia/strings_and_bytes.html#ixiapassphrase
[ixia-shuffled]: https://trag1c.github.io/ixia/sequences.html#ixiashuffled
[ixia-universe-rand]: https://trag1c.github.io/ixia/integers.html#ixiauniverse_rand
[uv]: https://docs.astral.sh/uv/
[just]: https://github.com/casey/just/
