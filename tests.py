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
def test_do_or(tree, expected):
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
def test_do_and(tree, expected):
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
def test_do_xor(tree, expected):
    assert caesium.do_xor(tree) is expected


@pytest.mark.parser
@pytest.mark.parametrize(
    "tree,expected",
    (
        (
            caesium.Node(caesium.Token("NAME", "FalSE"), []),
            False,
        ),
        (
            caesium.Node(
                caesium.Token("AND", "&"),
                [
                    caesium.Node(caesium.Token("NAME", "1"), []),
                    caesium.Node(caesium.Token("NAME", "FALSE"), []),
                ],
            ),
            False,
        ),
        (
            caesium.Node(
                caesium.Token("NOR", "~"),
                [
                    caesium.Node(
                        caesium.Token("NOT", "NOT"),
                        [caesium.Node(caesium.Token("NAME", "true"), [])],
                    ),
                    caesium.Node(caesium.Token("NAME", "1"), []),
                ],
            ),
            False,
        ),
        (
            caesium.Node(
                caesium.Token("XOR", "XOR"),
                [
                    caesium.Node(
                        caesium.Token("LPAREN", "("),
                        [caesium.Node(caesium.Token("NAME", "true"), [])],
                    ),
                    caesium.Node(caesium.Token("NAME", "1"), []),
                ],
            ),
            False,
        ),
        (
            caesium.Node(
                caesium.Token("LPAREN", "("),
                [
                    caesium.Node(
                        caesium.Token("NOT", "NOT"),
                        [caesium.Node(caesium.Token("NAME", "true"), [])],
                    )
                ],
            ),
            False,
        ),
        (
            caesium.Node(
                caesium.Token("EQUALS", "="),
                [
                    caesium.Node(caesium.Token("NAME", "foobar"), []),
                    caesium.Node(caesium.Token("NAME", "true"), []),
                ],
            ),
            True,
        ),
    ),
)
def test_visit_tree(tree, expected):
    assert caesium.visit_tree(tree) is expected


@pytest.mark.ast
@pytest.mark.parametrize(
    "line,expected_tree",
    (
        (
            "tRuE",
            caesium.Node(caesium.Token("NAME", "tRuE"), []),
        ),
        (
            "1 ^ 0",
            caesium.Node(
                caesium.Token("XOR", "^"),
                [
                    caesium.Node(caesium.Token("NAME", "1"), []),
                    caesium.Node(caesium.Token("NAME", "0"), []),
                ],
            ),
        ),
        (
            "a_var = 0",
            caesium.Node(
                caesium.Token("EQUALS", "="),
                [
                    caesium.Node(caesium.Token("NAME", "a_var"), []),
                    caesium.Node(caesium.Token("NAME", "0"), []),
                ],
            ),
        ),
    ),
)
def test_build_ast(line, expected_tree):
    tree = caesium.build_ast(
        (
            caesium.Token(match.lastgroup, match.group())
            for match in iter(caesium.MASTER_REGEX.scanner(line).match, None)
            if match.lastgroup not in ("COMMENT", "WHITESPACE")
            # This line just strips out comments and whitespace to reduce the
            # amount of useless tokens in the stream.
        )
    )
    assert tree == expected_tree


if __name__ == "__main__":
    pytest.main()
