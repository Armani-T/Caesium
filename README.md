# Caesium README

Caesium is a simple language built to evaluate Boolean algebra.

## Installation

1. Ensure that you have a working version of python3 (If you don't, you can get it from the [official site](https://www.python.org/)). Any python version ≥ 3.4.3 should work.
2. Clone the repo using `git clone` or download it as a zip file and unzip it anywhere in your file system.
3. Navigate to the project's root folder and run `pip install -r requirements.txt` to install the dependencies.
4. Add the `./caesium.py` file to your `PATH` (**This step is optional**).

## Usage

### Starting the Prompt

You can start the prompt by running `caesium`. Please note that this route can only work if you follow Step 4 of the [Installation guide](#Installation).

You can also start the prompt by navigating to the root directory of this project and running `python3 caesium.py`.

Example:

```
$ caesium
caesium v0.4.1 running on win32.
Press Ctrl+C or type "exit" to quit.
Cs> 
```

If you want to close the interpreter now, skip down [here](#Exiting) to learn how to.

### Expressions

An expression is any valid piece of code which returns a value. Expressions are evaluated right to left unless brackets (`()`) are used. If brackets are used, they are evaluated from the innermost to the outermost pair.

#### Values

There are only 2 built-in values: `True` and `False` (or `1` and `0` respectively). Caesium is case-insensitive they will work both in upper and lower case.

There is also the `random` keyword which randomly evaluates to either `True` or `False` every time it's used.

```
Cs> TRUE
True
Cs> False
False
Cs> 0
True
Cs> 1
False
Cs> random
True
```

#### Assignment

You can assign a name to a value by putting a valid identifier on the left,then a `=` and finally an expression. A valid identifier is any string of Unicode text that is not a keyword and that has no whitespace characters within. Assignments can be chained together or nested within an expression.

```
Cs> foo = True
True
Cs> quux = coco = (True ^ (bar = True)) & False
False
```

#### Operators

In caesium (and Boolean algebra in general),there are 2 types of operators: *basic* and *derived* operators.

#### Basic Operators

Basic operators, together with the 2 Boolean values, are the building blocks of Boolean algebra. There are only 3 of these basic operators. They are:

##### 1. `NOT`

`NOT` takes  one value and flips its value. `NOT` can also be written as `!`. `NOT` operations can be tabulated as:

Expression | Result |
|:---:|:---:|
`!True` | `False` |
`!False` | `True` |

##### 2. `AND`

`AND` takes 2 arguments and checks if both of them evaluate to `True`. If they both do, it returns `True`, otherwise it returns `False`. `AND` can also be written as `&` or `&&`. `AND`  operations can be tabulated as:

Expression | Result |
|:---:|:---:|
`True AND True` | `True` |
`True AND False` | `False` |
`False AND True` | `False` |
`False AND False` | `False` |


##### 3. `OR`

`OR` also takes 2 arguments and checks if both of them evaluate to `False`. If they both do, it returns `False`, otherwise it returns `True`. `OR` can also be written as `|` or `||`. `OR` operations can be tabulated as:

Expression | Result |
|:---:|:---:|
`True || True` | `True` |
`True || False` | `True` |
`False || True` | `True` |
`False || False` | `False` |

#### Derived Operators

Derived operators, as their name implies, are derived from basic operators. All of them can be rewritten using only the basic operators.

##### 1. `XOR`

`XOR`, or **eXclusive OR**, works just like `OR`, but both values cannot be `True`. `XOR` can also be written as `^`. `XOR` operations can be represented in a table as:

Expression | Result |
|:--------:|:------:|
`True ^ True` | `False` |
`True ^ False` | `True` |
`False ^ True` | `True` |
`False ^ False` | `False` |

##### 2. `NOR`

`NOR` also works like `OR`, but it returns the opposite of what `OR` would. You can mimic it by doing `!(<val_1> || <val_2>)`. It can also be written as `~`. `NOR` operations can be represented in a table as:

Expression | Result |
|:---:|:---:|
`True NOR True` | `False` |
`True NOR False` | `False` |
`False NOR True` | `False` |
`False NOR False` | `True` |

##### 3. `NAND`

`NAND` works exactly like `AND`, but it returns the opposite of what `AND` would. You can mimic it by doing `NOT (<val_1> AND <val_2>)`. It can also be written as `@`. NAND operations can be represented in a table as:

Expression | Result |
|:---:|:---:|
`True @ True` | `False` |
`True @ False` | `True` |
`False @ True` | `True` |
`False @ False` | `True` |

### Comments

Comments are lines of text meant for other people to read, rather than for the interpreter to run. If a line begins with a `#` character, the entire line is treated by the interpreter as if it is empty.

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

Either pressing `Control + C` or typing in `exit` and hitting Enter will cause the interpreter to stop and take you back to the normal shell. Using either route, the interpreter should stop running almost instantly.

```
Cs> exit
$
```

## TODO

- [ ] Add a proper parse tree.
- [ ] Put Caesium on PyPI.

## Development Setup

1. Create a virtualenv.
2. Install the development packages by running `pip install -r requirements-dev.txt`.
3. Assert everything is working by running  `pytest tests.py` from the project's root dir.

## Contributing

1. Crete your feature branch by forking the `develop` branch.
2. Run `black` on all the code in the repo.
3. Commit your changes.
4. Push to `origin/develop`.
5. Open a pull request.

## Notes

Just lke the element Caesium, this app may also break down. In case it does, don't heitate to contact me (though I might be a bit slow) or patch it yourself if you so wish.

## Meta

- Name: **Armani Tallam**
- E-Mail: <armanitallam@gmail.com>
- GitHub: <https://www.github.com/Armani-T>

This project is licensed under the **BSD License**. See the [license text](./LICENSE.txt) for more information.
