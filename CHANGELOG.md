# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

### Added
* Python 3.13 support

### Changed
* `rand_bool` now accepts an optional `p` argument for setting the probability
  of being true

### Fixed
* Corrected a syntax error in `ixia.sample`'s docstring

### Removed
* Python 3.8 support

## [1.3.2] - 2024-06-03

### Added
- A `py.typed` marker
- Missing docstrings for `ixia.rand_date` and `ixia.rand_time`
- `ixia.passphrase` now also accepts any path-like object

### Fixed
- Corrected a typo in `ixia.sample`'s docstring
- Corrected `ixia.passphrase` path handling for non-macOS targets
- Included `ixia.binomial_variate` in `__all__` and made it correctly importable

## [1.3.1] - 2023-10-02

### Fixed
- Included `rand_ints` in `__all__`

## [1.3.0] - 2023-10-02

### Added
- `ixia.choice` now accepts a `weights` or a `cumulative_weights` argument
- `ixia.rand_ints(a, b, k)`, equivalent to
  `[ixia.rand_int(a, b) for _ in range(k)]`
- Updated the project to be based on the Python 3.12 implementation:
  - Added a default value of `1.0` for `ixia.expo_variate`
  - Added `ixia.binomial_variate`

### Changed
- `ixia.choice` now does an early check for an empty sequence
- Improved speed for `ixia.rand_bool` (~35% faster) and
  `ixia.choices` (~3% faster)

## [1.2.0] - 2023-03-12

### Added
- `rand_date(start: Datelike, end: Datelike | None = None) -> datetime.date`
- `rand_time(start: Timelike | None = None, end: Timelike | None = None) -> datetime.time`

### Changed
- Improved project structure

## [1.1.0] - 2023-03-02

### Added
- `rand_bool() -> bool`
- `rand_line(file: TextIOBase | str) -> str`
- Default values for `gauss` and `normal_variate` (to comply with Python 3.11)

## [1.0.0] - 2022-10-31

Initial release 🎉

[1.0.0]: https://github.com/trag1c/ixia/releases/tag/1.0.0
[1.1.0]: https://github.com/trag1c/ixia/compare/1.0.0...1.1.0
[1.2.0]: https://github.com/trag1c/ixia/compare/1.1.0...1.2.0
[1.3.0]: https://github.com/trag1c/ixia/compare/1.2.0...1.3.0
[1.3.1]: https://github.com/trag1c/ixia/compare/1.3.0...1.3.1
[1.3.2]: https://github.com/trag1c/ixia/compare/1.3.1...1.3.2
