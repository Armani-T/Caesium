#!/usr/bin/env python3
from argparse import ArgumentParser
from collections import namedtuple
from re import IGNORECASE, compile as re_compile
from random import choice
from sys import platform, stdin, stdout
from typing import Generator, Iterable, Sequence

PROGRAM_NAME, VERSION = "caesium", "v0.3.2"
KEYWORDS = ("true", "false", "and", "or", "not", "xor", "exit", "random")
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
        r"(?P<INVALID_CHAR>.)",
    )
)
MASTER_REGEX = re_compile(REGEX_TOKENS, IGNORECASE)

Token = namedtuple("Token", ("type", "text"))
runtime_vars = {}

is_keyword = lambda name: name.lower() in KEYWORDS
get_name = lambda name: runtime_vars[name.lower()]
store_name = lambda name, value: runtime_vars.update({name.lower(): value})


def tokenize(text: str) -> Generator[Token, None, None]:
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
    scanner = MASTER_REGEX.scanner(text)
    for match in iter(scanner.match, None):
        if match.lastgroup == "INVALID_CHAR":
            raise SyntaxError('Invalid syntax: "%s".' % match.group())
        if match.lastgroup not in ("COMMENT", "WHITESPACE"):
            yield Token(match.lastgroup, match.group())


def parse_expr(expr: Iterable[Token]) -> bool:
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
    if not tokens:
        raise SyntaxError("Empty expression.")
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

    def stop():
        import sys

        stdout.write("Exiting...\n")
        sys.exit(0)

    name = name.lower()
    return {
        "true": lambda _: True,
        "1": lambda _: True,
        "false": lambda _: False,
        "0": lambda _: False,
        "exit": lambda _: stop(),
        "random": lambda _: choice((True, False)),
    }.get(name, get_name)(name)


def parse_operation(expr: Sequence[Token]) -> bool:
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
        return do_assignment(expr)

    if expr[1].type == "AND":
        return do_and(expr)

    if expr[1].type == "OR":
        return do_or(expr)

    if expr[1].type == "XOR":
        return do_xor(expr)

    line = " ".join((token.text for token in expr))
    raise SyntaxError('Invalid syntax: "%s".' % line)


def do_assignment(expr: Sequence[Token]) -> bool:
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


def do_parens(expr: Sequence[Token]) -> bool:
    """Evaluate the expression inside a pair of parentheses."""
    skips = expr.count(Token("LPAREN", "(")) - 1
    rparen_index = expr.index(Token("RPAREN", ")"))
    while skips > 0:
        lparen_index = expr.index(Token("LPAREN", "("))
        expr_ = expr[lparen_index:]
        rparen_index = expr_.index(("RPAREN", ")")) + 1
        skips -= 1

    return parse_expr(expr[1:rparen_index])


def do_and(expr: Sequence[Token]) -> bool:
    """Evaluate the value of an AND expression."""
    return parse_name(expr[0].text) and parse_expr(expr[2:])


def do_or(expr: Sequence[Token]) -> bool:
    """Evaluate the value of an OR expression."""
    return parse_name(expr[0].text) or parse_expr(expr[2:])


def do_xor(expr: Sequence[Token]) -> bool:
    """Evaluate the value of an XOR expression."""
    left = parse_name(expr[0].text)
    right = parse_expr(expr[2:])
    return (left or right) and (not (left and right))


def run_prompt(line: str) -> str:
    """Get code from the prompt, run then return it."""
    try:
        tokens = tokenize(line)
        return str(parse_expr(tokens)) or ""

    except (SyntaxError, NameError) as error:
        return error.args[0]
    except KeyError as error:
        return 'Undefined name "%s".' % error.args[0]
    except ValueError:
        return "Unmatched bracket in expression."


def main() -> None:
    """Start and manage the language's REPL."""
    stdout.write(
        "%s %s running on %s.\nPress Ctrl+C to exit."
        % (PROGRAM_NAME, VERSION, platform)
    )
    running = True
    while running:
        try:
            stdout.write(PROMPT)
            line = stdin.readline()
            if line:
                expr_value = run_prompt(line)
                stdout.write(expr_value)

        except KeyboardInterrupt:
            stdout.write("\nExiting...\n")
            running = False


if __name__ == "__main__":
    parser = ArgumentParser(prog=PROGRAM_NAME)
    parser.add_argument(
        "-v",
        "--version",
        action="store_true",
        help="Print %(prog)s's version number.",
    )
    parser.add_argument(
        "-e",
        "--expr",
        default="",
        help="Run the provided expression, print the result and exit.",
    )
    args = parser.parse_args()

    if args.version:
        stdout.write("%s %s\n" % (PROGRAM_NAME, VERSION))
    elif args.expr:
        parsed_value = parse_expr(tokenize(args.expr))
        stdout.write(str(parsed_value))
        stdout.write("\n")
    else:
        main()
