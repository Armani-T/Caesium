from typing import List, Tuple

import pytest

import caesium


@pytest.mark.parametrize(
    "source,tokens",
    (
        (
            "E_VAR = Elephant = TRUE",
            (
                caesium.Token("NAME", "e_var"),
                caesium.Token("EQUALS", "="),
                caesium.Token("NAME", "elephant"),
                caesium.Token("EQUALS", "="),
                caesium.Token("NAME", "true"),
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
        ("!a", (caesium.Token("NOT", "!"), caesium.Token("NAME", "a"))),
        ("false", (caesium.Token("NAME", "false"),)),
    ),
)
def test_tokenize(source: str, tokens: Tuple[caesium.Token]):
    stream = tuple(caesium.tokenize(source))
    assert stream == tokens


@pytest.mark.parametrize("text", ("1 `OR` 0", "1 - 0", "~1/", "+1"))
def test_tokenize_raises_syntaxerror_on_invalid_char(text: str):
    with pytest.raises(SyntaxError):
        tuple(caesium.tokenize(text))


@pytest.mark.parametrize(
    "flags,attr_name",
    ((["-v"], "version"), (["--expr", "true ^ false | 0 & 1"], "expr")),
)
def test_valid_cli_flags(flags: List[str], attr_name: str):
    arg_parser = caesium.setup_cli()
    args = arg_parser.parse_args(flags)
    assert getattr(args, attr_name)


@pytest.mark.parametrize("flags", (["-a"], ["--wrong"], ["--expr"]))
def test_invalid_cli_flags(flags: List[str]):
    with pytest.raises(SystemExit):
        parser = caesium.setup_cli()
        parser.parse_args(flags)


if __name__ == "__main__":
    pytest.main(["-ra"])
