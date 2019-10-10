import pytest

import caesium

parametrize = pytest.mark.parametrize
xfail = pytest.mark.xfail


@pytest.fixture(autouse=True)
def patch_runtime_vars(monkeypatch):
    new_vars = {
        "a_var": True,
        "another_var": True,
        "quux": False,
        "foobar": False,
    }
    monkeypatch.setattr(caesium, "RUNTIME_VARS", new_vars)


@parametrize(
    "name,expected",
    (("1", True), ("NOT", True), ("quux", False), ("foobar", False)),
)
def test_is_keyword(name: str, expected: bool):
    assert caesium.is_keyword(name) is expected


@parametrize("name,expected", (("a_var", True), ("quux", False)))
def test_get_name(name: str, expected: bool):
    assert caesium.get_name(name) is expected


@parametrize("name,value", (("abracadabra", True), ("epsilon", False)))
def test_store_name(name: str, value: bool):
    caesium.store_name(name, value)
    assert name in caesium.RUNTIME_VARS
    assert caesium.get_name(name) is value


@parametrize(
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
def test_tokenize(source: str, tokens: tuple):
    stream = tuple(caesium.tokenize(source))
    assert stream == tokens


@parametrize(
    "line",
    (
        "E_VAR = e_var = TRUE",
        "true",
        pytest.param("(True) | (False)", marks=xfail),
    ),
)
def test_parse_expr(line: str):
    tokens = tuple(caesium.tokenize(line))
    assert caesium.parse_expr(tokens)


@parametrize(
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


@parametrize(
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


@parametrize(
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


@parametrize(
    "flags,attr_name",
    (
        (["--version"], "version"),
        (["-v"], "version"),
        (["-e", "true"], "expr"),
        (["--expr", "true ^ false | 0 & 1"], "expr"),
    ),
)
def test_valid_cli_flags(flags, attr_name):
    arg_parser = caesium.setup_cli()
    args = arg_parser.parse_args(flags)
    assert getattr(args, attr_name)


@parametrize("flag", (["-a"], ["--wrong"], ["--expr"]))
def test_invalid_cli_flag(flag):
    with pytest.raises(SystemExit):
        arg_parser = caesium.setup_cli()
        args = arg_parser.parse_args(flag)


@parametrize("expr", ("TRUE=0", "1 = 0", "false=random"))
def test_invalid_assignments(expr):
    tokens = tuple(caesium.tokenize(expr))
    with pytest.raises(NameError) as excinfo:
        caesium.do_assignment(tokens)
    assert "reserved" in str(excinfo.value)


@parametrize("text", ("1 `OR` 0", "1 - 0", "~/1/"))
def test_tokenize_raises_syntaxerror_on_invalid_char(text):
    with pytest.raises(SyntaxError):
        tuple(caesium.tokenize(text))


if __name__ == "__main__":
    pytest.main(["-ra"])
