from typing import List, Tuple

import pytest

import caesium


@pytest.mark.tokenizer
@pytest.mark.parametrize(
    "source,tokens",
    (
        (
            "E_VAR = Elephant = TRUE",
            (
                caesium.Token("NAME", "E_VAR"),
                caesium.Token("EQUALS", "="),
                caesium.Token("NAME", "Elephant"),
                caesium.Token("EQUALS", "="),
                caesium.Token("NAME", "TRUE"),
            ),
        ),
        (
            "a | b & c",
            (
                caesium.Token("NAME", "a"),
                caesium.Token("OR", "|"),
                caesium.Token("NAME", "b"),
                caesium.Token("AND", "&"),
                caesium.Token("NAME", "c"),
            ),
        ),
        (
            "!(quux)",
            (
                caesium.Token("NOT", "!"),
                caesium.Token("LPAREN", "("),
                caesium.Token("NAME", "quux"),
                caesium.Token("RPAREN", ")"),
            ),
        ),
        ("false", (caesium.Token("NAME", "false"),)),
    ),
)
@pytest.mark.tokenizer
def test_tokenize(source: str, tokens: Tuple[caesium.Token, ...]) -> None:
    stream = tuple(caesium.tokenize(source))
    assert stream == tokens


@pytest.mark.tokenizer
@pytest.mark.parametrize("text", ("1 `OR` 0", "1 - 0", "~1/", "+1"))
def test_tokenize_raises_syntaxerror_on_invalid_char(text: str) -> None:
    with pytest.raises(SyntaxError):
        tuple(caesium.tokenize(text))


@pytest.mark.visitor
@pytest.mark.parametrize(
    "tree,expected",
    (
        (
            caesium.Node(
                caesium.Token("OR", "||"),
                [
                    caesium.Node(caesium.Token("NAME", "false"), []),
                    caesium.Node(caesium.Token("NAME", "1"), []),
                ],
            ),
            True,
        ),
        (
            caesium.Node(
                caesium.Token("OR", "|"),
                [
                    caesium.Node(caesium.Token("NAME", "0"), []),
                    caesium.Node(
                        caesium.Token("LPAREN", "("),
                        [caesium.Node(caesium.Token("NAME", "false"), [])],
                    ),
                ],
            ),
            False,
        ),
    ),
)
def test_do_or(tree: caesium.Node, expected: bool) -> None:
    assert caesium.do_or(tree) is expected


@pytest.mark.visitor
@pytest.mark.parametrize(
    "tree,expected",
    (
        (
            caesium.Node(
                caesium.Token("AND", "AND"),
                [
                    caesium.Node(caesium.Token("NAME", "false"), []),
                    caesium.Node(caesium.Token("NAME", "1"), []),
                ],
            ),
            False,
        ),
        (
            caesium.Node(
                caesium.Token("AND", "&&"),
                [
                    caesium.Node(caesium.Token("NAME", "true"), []),
                    caesium.Node(
                        caesium.Token("EQUALS", "="),
                        [
                            caesium.Node(caesium.Token("NAME", "x"), []),
                            caesium.Node(caesium.Token("NAME", "TRUE"), []),
                        ],
                    ),
                ],
            ),
            True,
        ),
    ),
)
def test_do_and(tree: caesium.Node, expected: bool) -> None:
    assert caesium.do_and(tree) is expected


@pytest.mark.visitor
@pytest.mark.parametrize(
    "tree,expected",
    (
        (
            caesium.Node(
                caesium.Token("XOR", "^"),
                [
                    caesium.Node(caesium.Token("NAME", "TRUE"), []),
                    caesium.Node(caesium.Token("NAME", "true"), []),
                ],
            ),
            False,
        ),
        (
            caesium.Node(
                caesium.Token("XOR", "XOR"),
                [
                    caesium.Node(caesium.Token("NAME", "true"), []),
                    caesium.Node(
                        caesium.Token("AND", "AND"),
                        [
                            caesium.Node(caesium.Token("NAME", "1"), []),
                            caesium.Node(caesium.Token("NAME", "false"), []),
                        ],
                    ),
                ],
            ),
            True,
        ),
    ),
)
def test_do_xor(tree: caesium.Node, expected: bool) -> None:
    assert caesium.do_xor(tree) is expected


@pytest.mark.cli
@pytest.mark.parametrize(
    "flags,attr_name",
    ((["-v"], "version"), (["--expr", "true ^ false | 0 & 1"], "expr")),
)
def test_valid_cli_flags(flags: List[str], attr_name: str) -> None:
    arg_parser = caesium.setup_cli()
    args = arg_parser.parse_args(flags)
    assert getattr(args, attr_name)


@pytest.mark.cli
@pytest.mark.parametrize("flags", (["-a"], ["--wrong"], ["--expr"]))
def test_invalid_cli_flags(flags: List[str]) -> None:
    with pytest.raises(SystemExit):
        parser = caesium.setup_cli()
        parser.parse_args(flags)


if __name__ == "__main__":
    pytest.main(["-ra"])
