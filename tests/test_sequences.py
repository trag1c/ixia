from pathlib import Path
from unittest.mock import patch

import pytest

from ixia import passphrase, rand_line, shuffled

TEST_LIST = [6, 3, 9, 1, 2, 4, 8, 0, 5, 7]


def test_shuffled() -> None:
    for _ in range(300):
        s = shuffled(TEST_LIST)
        assert TEST_LIST is not s
        assert sorted(s) == sorted(TEST_LIST)


def test_rand_line(tmp_path: Path) -> None:
    lines = ("hello", "there", "general", "kenobi")
    (path := tmp_path / "sample.txt").write_text("\n".join(lines))

    assert rand_line(str(path)) in lines
    with path.open() as f:
        assert rand_line(f)


def test_passphrase(tmp_path: Path) -> None:
    (path := tmp_path / "words.txt").write_text("one\ntwo\nthree\nfour\nfive")
    assert not passphrase(0, words_path=path)
    assert passphrase(1, words_path=path)


def test_passphrase_nonexistent() -> None:
    with patch("ixia.strings.Path") as path_mock:
        path_inst = path_mock.return_value
        path_inst.exists.return_value = False
        path_inst.__eq__.return_value = True
        with pytest.raises(NotImplementedError):
            passphrase(1)
