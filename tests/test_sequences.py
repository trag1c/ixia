from sys import platform

from pytest import raises

from ixia import choice, choices, passphrase, sample, shuffled

TEST_LIST = [6, 3, 9, 1, 2, 4, 8, 0, 5, 7]


def test_choice():
    for _ in range(30):
        assert choice(TEST_LIST) in TEST_LIST


def test_choices():
    with raises(TypeError):
        choices(TEST_LIST, [1] * 10, cumulative_weights=[1] * 10)
    with raises(ValueError):
        choices(TEST_LIST, [1])
    with raises(ValueError):
        choices(TEST_LIST, cumulative_weights=[0.0])
    with raises(ValueError):
        choices(TEST_LIST, cumulative_weights=[1e309])
    for _ in range(50):
        assert set(choices(TEST_LIST, k=10)) <= set(TEST_LIST)


def test_sample():
    with raises(ValueError):
        sample(TEST_LIST, len(TEST_LIST) + 1)
    assert sorted(sample(TEST_LIST, len(TEST_LIST))) == TEST_LIST
    assert sample(TEST_LIST, k=1, counts=[1] + [0] * (len(TEST_LIST) - 1)) == TEST_LIST[0]


def test_shuffled():
    for _ in range(300):
        s = shuffled(TEST_LIST)
        assert TEST_LIST is not s
        assert sorted(s) == sorted(TEST_LIST)


def test_passphrase():
    if platform not in ("linux", "darwin", "aix"):
        with raises(NotImplementedError):
            passphrase(0)
    else:
        assert not passphrase(0)
        assert passphrase(1)