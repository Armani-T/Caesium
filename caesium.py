#!/usr/bin/env python3
from collections import namedtuple
from collections.abc import Sequence, Iterator
from datetime import datetime
from re import IGNORECASE, compile as re_compile
from sys import platform, stdin, stdout

NAME = "Caesium"
VERSION = "0.1.1"
KEYWORDS = ("true", "false", "and", "or", "not", "xor")
PROMPT = "\n>> "
REGEX_TOKENS = "|".join(
    (
        r"(?P<NOT>\bnot\b|\!)",
        r"(?P<OR>\bor\b|\|\||\|)",
        r"(?P<AND>\band\b|\&\&|\&)",
        r"(?P<XOR>\bxor\b|\^)",
        r"(?P<NAME>\b\w+\b)",
        r"(?P<EQUALS>\=)",
        r"(?P<LPAREN>\()",
        r"(?P<RPAREN>\))",
        r"(?P<WHITESPACE>\s+)",
        r"(?P<COMMENT>#(.)*?\n)",
    )
)
MASTER_REGEX = re_compile(REGEX_TOKENS, IGNORECASE)

Token = namedtuple("Token", ("type", "text"))
runtime_vars = {}

is_keyword = lambda name: name.lower() in KEYWORDS
get_name = lambda name: runtime_vars[name.lower()]
store_name = lambda name, value: runtime_vars.update({name.lower(): value})


def tokenize(text: str, regex=MASTER_REGEX) -> Iterator:
    """
    Convert the source code into a stream of tokens.

    Parameters
    ----------
    text
        The source code to tokenize.
    regex
        A compiled regex used to make the text scanner.

    Yields
    ------
    Token
        A namedtuple with only 2 attributes: `type` and `text`.
    """
    scanner = regex.scanner(text)
    for match in iter(scanner.match, None):
        if match.lastgroup not in ("COMMENT", "WHITESPACE"):
            yield Token(match.lastgroup, match.group())


def parse_expr(expr: Sequence) -> bool:
    """
    Evaluate a single expression consisting of tokens.

    Parameters
    ----------
    expr
        A sequence of tokens representing a single expression.
    Returns
    -------
    bool
        The full expression's evaluated value or None if the expression
        is empty.
    """
    tokens = tuple(expr)
    if len(tokens) == 1:
        return parse_name(tokens[0].text)
    return parse_operation(tokens)


def parse_name(name: str) -> bool:
    """
    Evaluate the value of `name`.

    Parameters
    ----------
    name
        The name to be evaluated.

    Returns
    -------
    bool
        The name's evaluated value.
    """
    var = name.lower()
    if var in ("true", "1"):
        return True
    if var in ("false", "0"):
        return False
    return get_name(var)


def parse_operation(expr: Sequence) -> bool:
    """
    Evaluate part of or the whole of an expression.

    Parameters
    ----------
    expr
        The sequence of tokens representing a single expression.
    Returns
    -------
    bool
        The expression's evaluated value.
    """
    if expr[0].type == "LPAREN":
        return do_parens(expr)

    if expr[0].type == "NOT":
        return not parse_expr(expr[1:])

    if expr[1].type == "EQUALS":
        return parse_assign(expr)

    if expr[1].type == "AND":
        return do_and(expr)

    if expr[1].type == "OR":
        return do_or(expr)

    if expr[1].type == "XOR":
        return do_xor(expr)

    line = " ".join((token.text for token in expr))
    raise SyntaxError('Illegal expression: "%s".' % line)


def parse_assign(expr: Sequence) -> bool:
    """
    Evaluate and carry out an assignment expression.
    Parameters
    ----------
    expr
        The sequence of tokens representing a single expression.

    Returns
    -------
    bool
        The expression's evaluated value.
    """
    var_name = expr[0].text
    var_value = parse_expr(expr[2:])

    if is_keyword(var_name):
        raise NameError('Name "%s" is reserved.' % var_name)

    store_name(var_name, var_value)
    return var_value


def do_parens(expr: Sequence) -> bool:
    """Evaluate the expression inside a pair of parentheses."""
    skips = expr.count(Token("LPAREN", "(")) - 1
    rparen_index = expr.index(Token("RPAREN", ")"))
    while skips > 0:
        lparen_index = expr.index(Token("LPAREN", "("))
        expr_ = expr[lparen_index:]
        rparen_index = expr_.index(("RPAREN", ")")) + 1
        skips -= 1

    return parse_expr(expr[1:rparen_index])


def do_and(expr: Sequence) -> bool:
    """Evaluate the value of an AND expression."""
    return parse_name(expr[0].text) and parse_expr(expr[2:])


def do_or(expr: Sequence) -> bool:
    """Evaluate the value of an OR expression."""
    return parse_name(expr[0].text) or parse_expr(expr[2:])


def do_xor(expr: Sequence) -> bool:
    """Evaluate the value of an XOR expression."""
    left = parse_name(expr[0].text)
    right = parse_expr(expr[2:])
    return (left or right) and not (left and right)


def main() -> None:
    """Start and manage the language's REPL."""
    stdout.write(
        "%s version %s running on %s.\nPress Ctrl+C to exit."
        % (NAME, VERSION, platform)
    )
    running = True

    while running:
        try:
            stdout.write(PROMPT)
            line = stdin.readline().strip()
            if not line:
                continue
            tokens = tokenize(line.strip())
            value = parse_expr(tokens)

        except (SyntaxError, NameError) as error:
            stdout.write("Error: %s" % error.args[0])
        except KeyError as error:
            stdout.write('Error: Undefined name "%s" entered.' % error.args[0])
        except KeyboardInterrupt:
            stdout.write("\nExiting...\n")
            running = False

        else:
            store_name("_", value)
            stdout.write(str(value))


if __name__ == "__main__":
    main()
