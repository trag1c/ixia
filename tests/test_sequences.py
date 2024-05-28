from pathlib import Path

from ixia import passphrase, shuffled

TEST_LIST = [6, 3, 9, 1, 2, 4, 8, 0, 5, 7]


def test_shuffled() -> None:
    for _ in range(300):
        s = shuffled(TEST_LIST)
        assert TEST_LIST is not s
        assert sorted(s) == sorted(TEST_LIST)


def test_passphrase(tmp_path: Path) -> None:
    (path := tmp_path / "words.txt").write_text("one\ntwo\nthree\nfour\nfive")
    assert not passphrase(0, words_path=path)
    assert passphrase(1, words_path=path)
