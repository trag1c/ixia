from sys import platform

from pytest import raises

from ixia import passphrase, shuffled

TEST_LIST = [6, 3, 9, 1, 2, 4, 8, 0, 5, 7]


def test_shuffled() -> None:
    for _ in range(300):
        s = shuffled(TEST_LIST)
        assert TEST_LIST is not s
        assert sorted(s) == sorted(TEST_LIST)


def test_passphrase() -> None:
    if platform not in ("linux", "darwin", "aix"):
        with raises(NotImplementedError):
            passphrase(0)
    else:
        assert not passphrase(0)
        assert passphrase(1)
