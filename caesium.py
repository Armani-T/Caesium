#!/usr/bin/env python3
from argparse import ArgumentParser
from collections import namedtuple
from re import IGNORECASE, compile as re_compile
from random import choice
from sys import platform, exit as sys_exit
from typing import Generator, Iterable, Pattern

__author__ = "Armani Tallam"
__program__ = "caesium"
__version__ = "1.1.0"

PROMPT = "Cs>"
MASTER_REGEX = re_compile(
    "|".join(
        (
            r"(?P<NOT>\bnot\b|!)",
            r"(?P<OR>\bor\b|\|\||\|)",
            r"(?P<AND>\band\b|&&|&)",
            r"(?P<XOR>\bxor\b|\^)",
            r"(?P<NAND>\bnand\b|@)",
            r"(?P<NOR>\bnor\b|~)",
            r"(?P<EQUALS>=)",
            r"(?P<NAME>\b\w+\b)",
            r"(?P<LPAREN>\()",
            r"(?P<RPAREN>\))",
            r"(?P<WHITESPACE>\s+)",
            r"(?P<COMMENT>#.*$)",
            r"(?P<INVALID_CHAR>.)",
        )
    ),
    IGNORECASE,
)

Token = namedtuple("Token", ("type", "value"))
Node = namedtuple("Node", ("token", "children"))
RUNTIME_VARS = {"true": True, "1": True, "false": False, "0": False}


def tokenize(text: str, regex: Pattern[str]) -> Generator[Token, None, None]:
    """
    Convert the source code into a stream of tokens.

    Parameters
    ----------
    text
        The source code to tokenize.
    regex
        A combination of all the language tokens. It will be used to
        generate tokens.

    Yields
    ------
    Token
        A namedtuple with only 2 attributes: `type` and `text`.
    """
    scanner = regex.scanner(text)
    for match in iter(scanner.match, None):
        if match.lastgroup == "INVALID_CHAR":
            raise SyntaxError('Error: Invalid syntax: "%s".' % match.group())
        if match.lastgroup not in ("COMMENT", "WHITESPACE"):
            yield Token(match.lastgroup, match.group())


def build_ast(tokens: Iterable[Token]) -> Node:
    """
    Convert the token stream into an AST for parsing.

    Parameters
    ----------
    tokens
        A stream of tokens from the tokener.

    Returns
    -------
    Node
        The root node of the code's AST.
    """
    parents = [Node(Token("ROOT", ""), [])]
    # The root node is always the first parent.

    for token in tokens:
        parent_node = parents[-1]
        current_node = Node(token, [])

        if token.type in ("AND", "OR", "XOR", "NAND", "NOR", "EQUALS"):
            current_node.children.append(parent_node.children.pop())
            parent_node.children.append(current_node)
            parents.append(current_node)
        elif token.type in ("NOT", "LPAREN"):
            parent_node.children.append(current_node)
            parents.append(current_node)
        elif token.type == "RPAREN":
            parent = parents.pop()
            while parent.token.type != "LPAREN":
                parent = parents.pop()
        else:
            parent_node.children.append(current_node)

    return parents[0]


def visit_tree(ast: Node) -> bool:
    """
    Evaluate part of or the whole of an expression.

    Parameters
    ----------
    ast
        A root node and its children which represent an expression.

    Returns
    -------
    bool
        The expression's evaluated value.
    """
    return {
        "AND": do_and,
        "EQUALS": do_equals,
        "LPAREN": lambda node: visit_tree(node.children[0]),
        "NAME": get_name,
        "NAND": lambda node: not do_and(node),
        "NOR": lambda node: not do_or(node),
        "NOT": lambda node: not visit_tree(node.children[0]),
        "ROOT": lambda node: visit_tree(node.children[0]),
        "OR": do_or,
        "XOR": do_xor,
    }[ast.token.type](ast)


def get_name(node: Node) -> bool:
    """
    Evaluate the value of a NAME node.

    Parameters
    ----------
    node
        The node to be evaluated.

    Returns
    -------
    bool
        The node's evaluated value.
    """
    name = node.token.value.lower()
    if name == "exit":
        sys_exit(0)
    if name == "random":
        return choice((True, False))
    # TODO: Find a way of removing these references to the global scope.
    return RUNTIME_VARS[name]


def do_equals(node: Node) -> bool:
    """
    Evaluate and carry out an assignment expression.

    Parameters
    ----------
    node
        The ast representing a single expression.

    Returns
    -------
    bool
        The expression's evaluated value.
    """
    keywords = (
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
    var_name = node.children[0].token.value.lower()
    var_value = visit_tree(node.children[1])

    if var_name in keywords:
        raise NameError('Error: Name "%s" is reserved.' % var_name)

    # TODO: Find a way of doing this without mutating the global scope.
    RUNTIME_VARS[var_name] = var_value
    return var_value


def do_and(node: Node) -> bool:
    """Evaluate the value of an AND expression."""
    return all((visit_tree(child) for child in node.children))


def do_or(node: Node) -> bool:
    """Evaluate the value of an OR expression."""
    return any((visit_tree(child) for child in node.children))


def do_xor(node: Node) -> bool:
    """Evaluate the value of an XOR expression."""
    children = [visit_tree(child) for child in node.children]
    return any(children) and not all(children)


def run_code(line: str) -> str:
    """
    Run and return line's string value.

    Parameters
    ----------
    line
        The line of code to be run.

    Returns
    -------
    str
        Either the string value of the evaluated line or an error
        message.
    """
    try:
        ast = build_ast(tokenize(line, MASTER_REGEX))
        return str(visit_tree(ast))
    except (NameError, SyntaxError) as error:
        return error.args[0]
    except KeyError as error:
        return 'Error: Undefined name "%s".' % error.args[0]


def setup_cli() -> ArgumentParser:
    """Set up and define the parser and command line flags for the app."""
    parser = ArgumentParser(prog=__program__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-v", "--version", action="store_true", help="Print %(prog)s's version number."
    )
    group.add_argument(
        "-e", "--expr", default="", help="Print the result of %(dest)s and exit."
    )
    return parser


def main() -> int:
    """Parse the command line args and run the app accordingly."""
    parser = setup_cli()
    args = parser.parse_args()
    if args.version:
        print("%s v%s" % (__program__, __version__))
    elif args.expr:
        print(run_code(args.expr))
    else:
        print(
            '%s v%s running on %s.\nPress Ctrl+C or enter "exit" to exit.'
            % (__program__, __version__, platform)
        )
        while True:
            try:
                print(run_code(input("%s " % PROMPT)))
            except KeyboardInterrupt:
                break

    return 0
