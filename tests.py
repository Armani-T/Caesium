from typing import List

import pytest

import caesium


@pytest.mark.parser
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


@pytest.mark.parser
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


@pytest.mark.parser
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


@pytest.mark.ast
@pytest.mark.parametrize(
    "line,exprected_tree",
    (
        (
            "tRuE",
            caesium.Node(
                caesium.Token("ROOT", ""),
                [caesium.Node(caesium.Token("NAME", "tRuE"), [])],
            ),
        ),
        (
            "1 ^ 0",
            caesium.Node(
                caesium.Token("ROOT", ""),
                [
                    caesium.Node(
                        caesium.Token("XOR", "^"),
                        [
                            caesium.Node(caesium.Token("NAME", "1"), []),
                            caesium.Node(caesium.Token("NAME", "0"), []),
                        ],
                    )
                ],
            ),
        ),
        (
            "a_var = 0",
            caesium.Node(
                caesium.Token("ROOT", ""),
                [
                    caesium.Node(
                        caesium.Token("EQUALS", "="),
                        [
                            caesium.Node(caesium.Token("NAME", "a_var"), []),
                            caesium.Node(caesium.Token("NAME", "0"), []),
                        ],
                    )
                ],
            ),
        ),
    ),
)
def test_build_ast(line: str, expected_tree: caesium.Node):
    tokens = caesium.build_ast(
        (
            caesium.Token(match.lastgroup, match.group())
            for match in iter(caesium.MASTER_REGEX.scanner(line).match, None)
            if match.lastgroup not in ("COMMENT", "WHITESPACE")
            # This line just strips out comments and whitespace to reduce the
            # amount of useless tokens in the stream.
        )
    )
    assert tokens == expected_tree


if __name__ == "__main__":
    pytest.main()
