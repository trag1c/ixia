# Ixia


## ⚠️ Important Notes
While supporting Python 3.8+, Ixia is based on the Python 3.10 implementation
of the `random` module. The following changes have been made to the module
since Python 3.8:
- `getrandbits` accepts 0 for `k`
- `choices` raises a `ValueError` if all weights are zero
- `sample` has a new `counts` parameter

Additionally, Ixia executes 3.9 and 3.10 deprecations, thus:
- `ixia.rand_range` doesn't convert non-integer types to equivalent integers
- `ixia.sample` doesn't support `set` as a sequence type
- `ixia.shuffle` doesn't support the `random` parameter