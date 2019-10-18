from typing import List, Tuple

import pytest

import caesium


@pytest.mark.parametrize(
    "name,value",
    (
        ("foobar", False),
        ("quux", False),
        ("a_var", True),
        ("another_var", True),
    ),
)
def test_store_name(name: str, value: bool):
    caesium.store_name(name, value)
    assert name in caesium.RUNTIME_VARS
    assert caesium.get_name(name) is value


@pytest.mark.parametrize(
    "name,expected",
    (("1", True), ("NOT", True), ("quux", False), ("foobar", False)),
)
def test_is_keyword(name: str, expected: bool):
    assert caesium.is_keyword(name) is expected


@pytest.mark.parametrize("name,expected", (("a_var", True), ("quux", False)))
def test_get_name(name: str, expected: bool):
    assert caesium.get_name(name) is expected


@pytest.mark.parametrize(
    "source,tokens",
    (
        (
            "E_VAR = e_var = TRUE",
            (
                caesium.Token("NAME", "E_VAR"),
                caesium.Token("EQUALS", "="),
                caesium.Token("NAME", "e_var"),
                caesium.Token("EQUALS", "="),
                caesium.Token("NAME", "TRUE"),
            ),
        ),
        (
            "False xor FOOBAR",
            (
                caesium.Token("NAME", "False"),
                caesium.Token("XOR", "xor"),
                caesium.Token("NAME", "FOOBAR"),
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
    "line",
    (
        "E_VAR = e_var = TRUE",
        "true",
        pytest.param("quux = (foo = 1) | (bar = 0)", marks=pytest.mark.xfail),
    ),
)
def test_parse_expr(line: str):
    assert caesium.parse_expr(tuple(caesium.tokenize(line)))


@pytest.mark.parametrize(
    "expr,expected",
    (
        ("_a = !false", True),
        ("some_var = some_other_var = 0", False),
        ("!(a_var&(a_var|foobar))", False),
        ("another_var | a_var", True),
        ("foobar ^ quux", False),
    ),
)
def test_parse_operation(expr: str, expected: bool):
    stream = tuple(caesium.tokenize(expr))
    assert caesium.parse_operation(stream) is expected


@pytest.mark.parametrize(
    "expr,expected",
    (
        ("a_var=True", True),
        ("b_var = False", False),
        ("_ = 1", True),
        ("d_var = false", False),
        ("E_VAR = e_var = TRUE", True),
        ("F_VAR = f_var = 0", False),
    ),
)
def test_do_assignment(expr: str, expected: bool) -> None:
    tokens = tuple(caesium.tokenize(expr))
    result = caesium.do_assignment(tokens)
    assert caesium.get_name(tokens[0].value) is expected is result


@pytest.mark.parametrize(
    "name,expected",
    (
        ("true", True),
        ("True", True),
        ("FAlSe", False),
        ("FALSE", False),
        ("a_var", True),
        ("quux", False),
    ),
)
def test_parse_name(name: str, expected: bool) -> None:
    assert caesium.parse_name(name) is expected


@pytest.mark.parametrize(
    "flags,attr_name",
    (
        (["--version"], "version"),
        (["-v"], "version"),
        (["-e", "true"], "expr"),
        (["--expr", "true ^ false | 0 & 1"], "expr"),
    ),
)
def test_valid_cli_flags(flags: List[str], attr_name: str):
    arg_parser = caesium.setup_cli()
    args = arg_parser.parse_args(flags)
    assert getattr(args, attr_name)


@pytest.mark.parametrize("flags", (["-a"], ["--wrong"], ["--expr"]))
def test_invalid_cli_flag(flags: List[str]):
    with pytest.raises(SystemExit):
        parser = caesium.setup_cli()
        parser.parse_args(flags)


@pytest.mark.parametrize("expr", ("TRUE=0", "1 = 0", "false=random"))
def test_invalid_assignments(expr: str):
    with pytest.raises(NameError) as excinfo:
        caesium.do_assignment(tuple(caesium.tokenize(expr)))
    assert "reserved" in str(excinfo.value)


@pytest.mark.parametrize(
    "code,expected",
    (
        ("quux & 1", False),
        ("true && a_var", True),
        ("true AND (NOT true OR false)", False),
    ),
)
def test_do_and(code: str, expected: bool):
    expr = tuple(caesium.tokenize(code))
    assert caesium.do_and(expr) is expected


@pytest.mark.parametrize(
    "code,expected",
    (
        ("quux | 1", True),
        ("false || a_var", True),
        ("true OR (NOT true AND false)", True),
    ),
)
def test_do_or(code: str, expected: bool):
    expr = tuple(caesium.tokenize(code))
    assert caesium.do_or(expr) is expected


@pytest.mark.parametrize(
    "code,expected",
    (("quux ^ 1", True), ("true XOR (NOT true NOR false)", False)),
)
def test_do_xor(code: str, expected: bool):
    expr = tuple(caesium.tokenize(code))
    assert caesium.do_xor(expr) is expected


if __name__ == "__main__":
    pytest.main(["-ra"])
