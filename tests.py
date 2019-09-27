from pytest import mark, fixture

import caesium


@fixture(autouse=True)
def patch_runtime_vars(monkeypatch):
    new_vars = {
        "a_var": True,
        "another_var": True,
        "quux": False,
        "foobar": False,
    }
    monkeypatch.setattr(caesium, "runtime_vars", new_vars)


@mark.parametrize(
    "name,expected",
    (
        ("TRUE", True),
        ("false", True),
        ("not", True),
        ("quux", False),
        ("foobar", False),
        ("x", False),
    ),
)
def test_is_keyword(name: str, expected: bool):
    assert caesium.is_keyword(name) is expected


@mark.parametrize(
    "name,expected",
    (
        ("a_var", True),
        ("another_var", True),
        ("foobar", False),
        ("quux", False),
    ),
)
def test_get_name(name: str, expected: bool):
    assert caesium.get_name(name) is expected


@mark.parametrize(
    "name,value",
    (
        ("some_var", True),
        ("abracadabra", True),
        ("epsilon", False),
        ("quux", False),
    ),
)
def test_store_name(name: str, value: bool):
    caesium.store_name(name, value)
    assert name in caesium.runtime_vars
    assert caesium.get_name(name) is value


@mark.parametrize(
    "source,tokens",
    (
        (
            "a = b",
            (
                caesium.Token("NAME", "a"),
                caesium.Token("EQUALS", "="),
                caesium.Token("NAME", "b"),
            ),
        ),
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
            "false^b",
            (
                caesium.Token("NAME", "false"),
                caesium.Token("XOR", "^"),
                caesium.Token("NAME", "b"),
            ),
        ),
        (
            "a | b",
            (
                caesium.Token("NAME", "a"),
                caesium.Token("OR", "|"),
                caesium.Token("NAME", "b"),
            ),
        ),
        (
            "a & b",
            (
                caesium.Token("NAME", "a"),
                caesium.Token("AND", "&"),
                caesium.Token("NAME", "b"),
            ),
        ),
        ("!a", (caesium.Token("NOT", "!"), caesium.Token("NAME", "a"))),
        ("false", (caesium.Token("NAME", "false"),)),
    ),
)
def test_tokenize(source: str, tokens: tuple):
    stream = tuple(caesium.tokenize(source))
    assert stream == tokens


@mark.parametrize(
    "line",
    (
        "E_VAR = e_var = TRUE",
        "true",
        "!!(a_var)",
        "quux = (foo = True) ^ (bar = False)",
    ),
)
def test_parse_expr(line: str):
    tokens = tuple(caesium.tokenize(line))
    assert caesium.parse_expr(tokens)


@mark.parametrize(
    "expr,expected",
    (
        ("_a = !false", True),
        ("some_var = some_other_var = False", False),
        ("!(a_var&(a_var|foobar))", False),
        ("another_var | a_var", True),
        ("foobar ^ quux", False),
    ),
)
def test_parse_operation(expr: str, expected: bool):
    stream = tuple(caesium.tokenize(expr))
    return_value: bool = caesium.parse_operation(stream)
    assert return_value is expected


@mark.parametrize(
    "expr,expected",
    (
        ("a_var=True", True),
        ("b_var = False", False),
        ("_ = true", True),
        ("d_var = false", False),
        ("E_VAR = e_var = TRUE", True),
        ("F_VAR = f_var = FALSE", False),
    ),
)
def test_do_assignment(expr: str, expected: bool) -> None:
    tokens = tuple(caesium.tokenize(expr))
    result = caesium.do_assignment(tokens)
    assert result is caesium.get_name(tokens[0].text)
    assert caesium.get_name(tokens[0].text) is expected


@mark.parametrize(
    "name,expected",
    (
        ("true", True),
        ("True", True),
        ("tRUe", True),
        ("TRUE", True),
        ("false", False),
        ("False", False),
        ("FalSE", False),
        ("FALSE", False),
        ("a_var", True),
        ("another_var", True),
        ("foobar", False),
        ("quux", False),
    ),
)
def test_parse_name(name: str, expected: bool) -> None:
    assert caesium.parse_name(name) is expected
