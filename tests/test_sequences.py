import sys

import pytest

from ixia import passphrase, shuffled

TEST_LIST = [6, 3, 9, 1, 2, 4, 8, 0, 5, 7]


def test_shuffled() -> None:
    for _ in range(300):
        s = shuffled(TEST_LIST)
        assert TEST_LIST is not s
        assert sorted(s) == sorted(TEST_LIST)


@pytest.mark.skipif(
    sys.platform not in {"linux", "darwin", "aix"},
    reason="Not implemented on this platform",
)
def test_passphrase() -> None:
    assert not passphrase(0)
    assert passphrase(1)


@pytest.mark.skipif(
    sys.platform in {"linux", "darwin", "aix"},
    reason="Not implemented on this platform",
)
def test_passphrase_not_implemented() -> None:
    with pytest.raises(NotImplementedError):
        passphrase(0)
