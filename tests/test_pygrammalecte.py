import pytest

from pygrammalecte import (
    grammalecte_text,
    grammalecte_file,
    GrammalecteGrammarMessage,
    GrammalecteSpellingMessage,
)

_content = """\
Coucou, je veut du fromage.
Je sais coder en VHDL.
Le VHDL est est compliquer.
"""


def assert_messages(messages):
    message = next(messages)
    print(message)
    assert isinstance(message, GrammalecteGrammarMessage)
    assert message.line == 1
    assert message.start == 11
    assert message.end == 15
    assert message.rule == "g2__conj_je__b2_a1_1"
    assert message.message
    assert message.suggestions

    message = next(messages)
    print(message)
    assert isinstance(message, GrammalecteSpellingMessage)
    assert message.line == 2
    assert message.start == 17
    assert message.end == 21
    assert message.word == "VHDL"
    assert message.message == "Mot inconnu : VHDL"

    message = next(messages)
    print(message)
    message = next(messages)
    print(message)
    message = next(messages)
    print(message)

    with pytest.raises(StopIteration):
        next(messages)


def test_text():
    assert_messages(grammalecte_text(_content))


def test_file_path(tmp_path):
    with open(tmp_path / "file.txt", "w", encoding="utf-8") as f:
        f.write(_content)

    assert_messages(grammalecte_file(tmp_path / "file.txt"))


def test_file_path_as_a_string(tmp_path):
    with open(tmp_path / "file.txt", "w", encoding="utf-8") as f:
        f.write(_content)

    assert_messages(grammalecte_file(str(tmp_path / "file.txt")))
