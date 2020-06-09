# Caesium

[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![Build Status](https://travis-ci.com/Armani-T/Caesium.svg?branch=master)](https://travis-ci.com/Armani-T/Caesium)

Caesium is a simple language built to help myself (and others) learn about and understand how Boolean algebra works. It does this by providing an interpreter for Boolean algebra.

## Installation

1. Ensure that you have a working version of python (You can get python3 from the [official site](https://www.python.org/downloads/) if you don't have it or want to upgrade). Any python version >= 3.4.0 should work.
2. Install caesium using pip by running `pip install caesium-lang` from the command line.
3. Test it out by running the command `caesium` in your command line.

## Usage

### Starting the Prompt

You can start the prompt by typing the word `caesium` into your terminal and pressing Enter. The caesium prompt should start and print something out to the screen like so:

```
$ caesium
caesium version 1.3.1 running on win32.
Press Ctrl+C or type "exit" to quit.
Cs>
```

If you wish to close the interpreter now, scroll down to the **Exiting** header or press [here](#Exiting) to learn how to do that.

### Expressions

An expression is any valid code which can be turned into a single value. With the exception of the `exit` keyword, all valid code is made up of expressions. Expressions are evaluated right to left by default unless brackets (`()`) are used.

### Values

There are only 2 built-in values: `True` (or `1`) and `False`  (or `0`). Caesium is case-insensitive so it will accept them in upper, lower and even mixed case.

There is also the `random` keyword which randomly evaluates to either `True` or `False` whenever it is used.

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

You can bind a name to a value by putting a valid name, then a `=` and any valid expression. A valid name is made up of any number of alphanumeric characters and underscores.Valid names also cannot be keywords. Assignments can be chained together to define more than one variable at once. Since assignments are expressions, they can be nested within larger expressions. I wouldn't recommend this though, it makes the line quite unreadable.

```
Cs> foo = True
True
Cs> quux = coco = (True ^ (bar = True)) & False
False
```

### Operators

In Boolean algebra,there are 2 types of operators, *basic* operators and *derived* operators.

#### Basic Operators

Basic operators, together with the 2 Boolean values, are the building blocks of Boolean algebra. Without them, Boolean algebra simply wouldn't exist. There are only 3 basic operators:

##### 1. `NOT`

`not` takes a value and flips its value. It can also be written as `!`. Its operations can be summarised as:

Expression | Result |
|:---:|:---:|
`not True` | `False` |
`not False` | `True` |

##### 2. `AND`

`and` takes 2 arguments and checks if both of them evaluate to `True`. `and` can also be written as `&` or `&&`. `and`  operations can be summarised as:

Expression | Result |
|:---:|:---:|
`True and True` | `True` |
`True and False` | `False` |
`False and True` | `False` |
`False and False` | `False` |


##### 3. `OR`

`or` also takes 2 arguments and checks if both of them evaluate to `False`. `or` can also be written as `|` or `||`. `or` operations can be summarised as:

Expression | Result |
|:---:|:---:|
`True or True` | `True` |
`True or False` | `True` |
`False or True` | `True` |
`False or False` | `False` |

#### Derived Operators

Derived operators are called "derived" because they are derived from the basic operators (they can be re-written as basic operators). Since we ,as programmers, are too lazy to write them out in full, we made them as a kind of shorthand.

##### 1. `XOR`

`xor`, or **eXclusive OR**, works just like `or`, but where both values cannot be `True`. `xor` can also be written as `^`. `xor` operations can be represented in a table as:

Expression | Result |
|:--------:|:------:|
`True xor True` | `False` |
`True xor False` | `True` |
`False xor True` | `True` |
`False xor False` | `False` |

##### 2. `NOR`

`nor`, or **Not OR**, also works just like `or`, but it negates what `or` returns. It can also be written as `~`.nand`nor` operations can be represented in a table as:

Expression | Result |
|:---:|:---:|
`True nor True` | `False` |
`True nor False` | `False` |
`False nor True` | `False` |
`False nor False` | `True` |

##### 3. `NAND`

`nand`, or **Not AND**, works exactly like `and`, but it negates what `and` returns. It can also be written as `@`. `nand` operations can be represented in a table as:

Expression | Result |
|:---:|:---:|
`True nand True` | `False` |
`True nand False` | `True` |
`False nand True` | `True` |
`False nand False` | `True` |

### Help

Rather than having to refer to the README every single time you don't remember what an operator does, caesium comes with the `help` command. It is used to print out a line of explanation about the operator passed to it.

It is useed by typing `help` then the operator in question like so:

```
Cs> help or
or checks if at least one value is true.
```

### Comments

Comments are lines of text meant for other people to read, rather than for the interpreter to run. Everything that comes after a `#` character is treated by the interpreter as if it is not there. So for example, if a line starts with a `#`, the entire line will be treated as if it were blank.

### Errors

When you try to run code which has a mistake (like a missing bracket), the interpreter complains about your code instead of running it. This is an error. An error is basically the interpreter alerting you that there was something wrong with the code and so it can't run it. Once an error is thrown, you will have to fix whatever is wrong with your expression then rerun it.

Examples:

```
Cs> quux
Error: Undefined name "quux".
Cs> random/  # Here I'm supposed to write "random"
Error: Invalid syntax: "/".
```

### Exiting

Either pressing `Control + C` or typing in `exit` and hitting Enter will cause the interpreter to stop instantly and take you back to the normal shell.

```
Cs> exit

$
```

* * * * *

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
