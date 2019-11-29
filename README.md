# Caesium

[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![Build Status](https://travis-ci.com/Armani-T/Caesium.svg?branch=master)](https://travis-ci.com/Armani-T/Caesium)

Caesium is a simple language built to help myself (and others) learn about and understand how Boolean algebra works.

## Installation

1. Ensure that you have a working version of python (You can get python3 from the [official site](https://www.python.org/downloads/) if you don't have it or want to upgrade). Any python version >= 3.4.0 should work.
2. Install caesium using pip by running `pip install caesium-lang` from the command line.
3. Test it out by running the command `caesium` in your command line.

## Usage

### Starting the Prompt

You can start the prompt by running `caesium`.

Example:

```
$ caesium
caesium v1.2.0 running on win32.
Press Ctrl+C or type "exit" to quit.
Cs>
```

If you want to close the interpreter now, skip down [here](#Exiting) to learn how to do that.

### Expressions

An expression is any valid code which returns a value. In Caesium's case, that means that all valid code since all valid code must be an expression. Expressions are evaluated right to left unless brackets (`()`) are used.

### Values

There are only 2 built-in values: `True` (or `1`) and `False`  (or `0`). Caesium is case-insensitive so it will accept them in upper, lower and even mixed case.

There is also the `random` keyword which randomly evaluates to either `True` or `False` whenever it's used.

```
Cs> TRUE
True
Cs> False
False
Cs> tRuE
True
Cs> 0
True
Cs> 1
False
Cs> random
True
```

### Assignment

You can assign a name to a value by putting a valid identifier on the left, then a `=` and any valid expression. A valid identifier is any string of Unicode text that is neither a keyword nor does it contain whitespace. Assignments can be chained together to define more than one variable at once. Since assignments are expressions, they can be nested within larger expressions.

```
Cs> foo = True
True
Cs> quux = coco = (True ^ (bar = True)) & False
False
```

### Operators

In caesium (and Boolean algebra in general),there are 2 types of operators, *basic* operators and *derived* operators.

#### Basic Operators

Basic operators, together with the 2 Boolean values, are the building blocks of Boolean algebra. There are only 3 basic operators:

##### 1. `NOT`

`NOT` takes  one value and flips its value. `NOT` can also be written as `!`. Its operations can be summarised as:

Expression | Result |
|:---:|:---:|
`NOT True` | `False` |
`NOT False` | `True` |

##### 2. `AND`

`AND` takes 2 arguments and checks if both of them evaluate to `True`. If they both do, it returns `True`, otherwise it returns `False`. `AND` can also be written as `&` or `&&`. `AND`  operations can be summarised as:

Expression | Result |
|:---:|:---:|
`True AND True` | `True` |
`True AND False` | `False` |
`False AND True` | `False` |
`False AND False` | `False` |


##### 3. `OR`

`OR` also takes 2 arguments and checks if both of them evaluate to `False`. If they both do, it returns `False`, otherwise it returns `True`. `OR` can also be written as `|` or `||`. `OR` operations can be summarised as:

Expression | Result |
|:---:|:---:|
`True OR True` | `True` |
`True OR False` | `True` |
`False OR True` | `True` |
`False OR False` | `False` |

#### Derived Operators

Derived operators are called "derived" because they are derived from the basic operators (i.e: they can be re-written as basic operators). As programmers however, we are too lazy to write them out in full, so we made them as a kind of shorthand.

##### 1. `XOR`

`XOR`, or **eXclusive OR**, works just like `OR`, but where both values cannot be `True`. `XOR` can also be written as `^`. `XOR` operations can be represented in a table as:

Expression | Result |
|:--------:|:------:|
`True XOR True` | `False` |
`True XOR False` | `True` |
`False XOR True` | `True` |
`False XOR False` | `False` |

##### 2. `NOR`

`NOR`, or **Not OR**, also works just like `OR`, but it negates what `OR` returns. It can also be written as `~`.NAND`NOR` operations can be represented in a table as:

Expression | Result |
|:---:|:---:|
`True NOR True` | `False` |
`True NOR False` | `False` |
`False NOR True` | `False` |
`False NOR False` | `True` |

##### 3. `NAND`

`NAND`, or **Not AND**, works exactly like `AND`, but it negates what `AND` returns. It can also be written as `@`. `NAND` operations can be represented in a table as:

Expression | Result |
|:---:|:---:|
`True NAND True` | `False` |
`True NAND False` | `True` |
`False NAND True` | `True` |
`False NAND False` | `True` |

### Comments

Comments are lines of text meant for other people to read, rather than for the interpreter to run. If a line begins with a `#` character, the entire line is treated by the interpreter as if it is blank.

### Errors

When you try to run code which has a mistake (like a missing bracket), the interpreter complains about your code instead of running it. This is an error. An error is basically the interpreter alerting you that there was something wrong with the code and so it can't run it. Once an error is thrown, you will have to fix whatever is wrong with your expression and rerun it.

Examples:

```
Cs> quux
Undefined name "quux".
Cs> random/  # Meant to say "random"
Invalid syntax: "/".
```

### Exiting

Either pressing `Control + C` or typing in `exit` and hitting Enter will cause the interpreter to stop instantly and take you back to the normal shell.

```
Cs> exit
$
```

* * * * *

## TODO

- An internal help mechanism so that you don't have to keep referring to the README.

## Development Setup

1. Inside of a fresh virtualenv, install development packages by running `pip install -r requirements-dev.txt`.
2. Assert everything is working by running  `pytest tests.py` from the project's root dir.

## Contributing

1. Crete your feature branch by forking the `develop` branch.
3. Commit your changes.
4. Push to `origin/develop`.
5. Open a pull request.

## Notes

Just like the element Caesium, this app may break down. In case it does, please contact me or if you want to, fix it yourself.

## Meta

- Name: **Armani Tallam**
- E-Mail: armanitallam@gmail.com
- GitHub: <https://www.github.com/Armani-T>

This project is licensed under the **BSD 3-Clause License**. Please see the [license file](./LICENSE.txt)
for more information.
