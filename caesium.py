#!/usr/bin/env python3
from collections import namedtuple
from collections.abc import Iterable
from re import IGNORECASE, compile as re_compile
from random import choice as random_choice

__author__ = "Armani Tallam"
__program__ = "caesium"
__version__ = "1.3.3"

MASTER_REGEX = re_compile(
    "|".join(
        (
            r"(?P<HELP>\bhelp\b)",
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


class HelpMessage(Exception):
    pass


def build_ast(tokens: Iterable) -> Node:
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
    parents = [Node(None, [])]
    # NOTE: The node won't be used again anywhere else so I removed the name.

    for token in tokens:
        parent_node = parents[-1]
        current_node = Node(token, [])

        if token.type in ("AND", "OR", "XOR", "NAND", "NOR", "EQUALS"):
            current_node.children.append(parent_node.children.pop())
            parent_node.children.append(current_node)
            parents.append(current_node)
        elif token.type in ("NOT", "LPAREN", "HELP"):
            parent_node.children.append(current_node)
            parents.append(current_node)
        elif token.type == "RPAREN":
            parent = parents.pop()
            while parent.token.type != "LPAREN":
                parent = parents.pop()
        elif token.type == "NAME":
            parent_node.children.append(current_node)
        else:
            raise SyntaxError('Error: Invalid syntax: "%s".' % token.value)

    return parents[0].children[0]


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
        "OR": do_or,
        "XOR": do_xor,
        "HELP": do_help,
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
        raise KeyboardInterrupt
    if name == "random":
        return random_choice((True, False))
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
        "help",
        "1",
        "0",
    )
    var_name = node.children[0].token.value.lower()
    var_value = visit_tree(node.children[1])

    if var_name in keywords:
        raise NameError('Error: Name "%s" is reserved.' % var_name)

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


def do_help(node: Node) -> None:
    """Evaluate a help command."""
    if node.children[0].token.type == "NAME":
        name = node.children[0].token.value.lower()
        raise HelpMessage(
            "`exit` is used to close the program and return to the terminal"
            if name == "exit" else
            "`random` evaluates randomly to either `True` or `False`."
            if name == "random" else
            f"{name} = {get_name(node.children[0])}"
        )
    raise HelpMessage(
        {
            "HELP": "`help` is used to get short info on what a keyword does.",
            "NOT": "`not` is used to flip values (true to false and vice versa",
            "OR": "`or` checks if at least one value is true.",
            "AND": "`and` checks if both values are true.",
            "XOR": "`xor` checks if the two values are not the same.",
            "NAND": "`nand` is just short for `not (<value> and <value>)`.",
            "NOR": "`nor` is just short for `not (<value> or <value>)`.",
            "EQUALS": "`=` binds a name to a value like this: <name> = <value>.",
        }[node.children[0].token.type]
    )

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
        scanner = MASTER_REGEX.scanner(line)
        tokens = (
            Token(match.lastgroup, match.group())
            for match in iter(scanner.match, None)
            if match.lastgroup not in ("COMMENT", "WHITESPACE")
            # NOTE: This filter strips out comments and whitespace
            #       since they are not needed in any other step.
        )
        ast = build_ast(tokens)
        return str(visit_tree(ast))

    except (NameError, SyntaxError, HelpMessage) as error:
        return error.args[0]

    except KeyError as error:
        return 'Error: Undefined name "%s".' % error.args[0]

    except IndexError:
        return ""
