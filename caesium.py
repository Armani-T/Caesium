#!/usr/bin/env python3
from argparse import ArgumentParser
from collections import namedtuple
from re import IGNORECASE, compile as re_compile
from random import choice
from sys import platform, stdin, stdout, exit as sys_exit
from typing import Generator, Iterable, Sequence

PROGRAM_NAME, VERSION = "caesium", "0.4.0"
KEYWORDS = (
    "true",
    "false",
    "and",
    "or",
    "not",
    "xor",
    "nand",
    "nor",
    "exit",
    "random",
    "1",
    "0",
)
PROMPT = "Cs>"
REGEX_TOKENS = "|".join(
    (
        r"(?P<NOT>\bnot\b|!)",
        r"(?P<OR>\bor\b|\|\||\|)",
        r"(?P<AND>\band\b|&&|&)",
        r"(?P<XOR>\bxor\b|\^)",
        r"(?P<NAND>\bnand\b|@)",
        r"(?P<NOR>\bnor\b|~)",
        r"(?P<NAME>\b\w+\b)",
        r"(?P<EQUALS>\=)",
        r"(?P<LPAREN>\()",
        r"(?P<RPAREN>\))",
        r"(?P<WHITESPACE>\s+)",
        r"(?P<COMMENT>#.*$)",
        r"(?P<INVALID_CHAR>.)",
    )
)
MASTER_REGEX = re_compile(REGEX_TOKENS, IGNORECASE)

Token = namedtuple("Token", ("type", "value"))
RUNTIME_VARS = {}

is_keyword = lambda name: name.lower() in KEYWORDS
get_name = lambda name: RUNTIME_VARS[name.lower()]
store_name = lambda name, value: RUNTIME_VARS.update({name.lower(): value})


def tokenize(text: str) -> Generator[Token, None, None]:
    """
    Convert the source code into a stream of tokens.

    Parameters
    ----------
    text
        The source code to tokenize.

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
        raise AttributeError
    if len(tokens) == 1:
        return parse_name(tokens[0].value)
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
        stdout.write("Exiting...\n")
        sys_exit(0)

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

    def throw_error(expr):
        line = " ".join((token.value for token in expr))
        raise SyntaxError('Invalid syntax: "%s".' % line)

    return {
        "EQUALS": do_assignment,
        "AND": do_and,
        "OR": do_or,
        "XOR": do_xor,
        "NAND": lambda expr: not do_and(expr),
        "NOR": lambda expr: not do_or(expr),
    }.get(expr[1].type, throw_error)(expr)


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
    var_name = expr[0].value
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
    return parse_name(expr[0].value) and parse_expr(expr[2:])


def do_or(expr: Sequence[Token]) -> bool:
    """Evaluate the value of an OR expression."""
    return parse_name(expr[0].value) or parse_expr(expr[2:])


def do_xor(expr: Sequence[Token]) -> bool:
    """Evaluate the value of an XOR expression."""
    left = parse_name(expr[0].value)
    right = parse_expr(expr[2:])
    return (left or right) and (not (left and right))


def _run_code(line: str) -> str:
    """
    Get code from the prompt, run and return its string value.

    Parameters
    ----------
    line
        The line of code to be run.

    Returns
    -------
    str
        Either the string value of the evaluated code or an error
        message.
    """
    try:
        return str(parse_expr(tokenize(line)))
    except (SyntaxError, NameError) as error:
        return error.args[0]
    except KeyError as error:
        return 'Undefined name "%s".' % error.args[0]
    except ValueError:
        return "Unmatched bracket in expression."
    except AttributeError:
        return ""


def run_prompt() -> None:
    """Start and manage the language's REPL."""
    stdout.write(
        "%s v%s running on %s.\nPress Ctrl+C to exit."
        % (PROGRAM_NAME, VERSION, platform)
    )
    while True:
        try:
            stdout.write("\n%s " % PROMPT)
            stdout.write(_run_code(stdin.readline()))

        except KeyboardInterrupt:
            stdout.write("\nExiting...\n")
            return


def setup_cli() -> ArgumentParser:
    """Set up and define the parser and command line flags for the app."""
    parser = ArgumentParser(prog=PROGRAM_NAME)
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-v",
        "--version",
        action="store_true",
        help="Print %(prog)s's version number.",
    )
    group.add_argument(
        "-e",
        "--expr",
        default="",
        help="Print the result of the provided expression and exit.",
    )
    return parser


def main() -> None:
    """Parse the command line args and run the app accordingly."""
    parser = setup_cli()
    args = parser.parse_args()
    if args.version:
        stdout.write("%s v%s\n" % (PROGRAM_NAME, VERSION))
    elif args.expr:
        stdout.write(_run_code(args.expr))
    else:
        run_prompt()
    return 0


if __name__ == "__main__":
    sys_exit(main())
