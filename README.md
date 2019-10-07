# Caesium README

Caesium is a simple language for evaluating expressions from Boolean algebra. I tried to make it as compatible as possible with other programming languages. I built it to run my Boolean expressions when prototyping complex if statements.

## Installation

1. Ensure that you have a working version of python3 (If not, you can get it from the [official site](https://www.python.org/)). Any python version >= 3.4 should work.
2. Just clone the repo using `git clone`.
3. Install the dependencies by navigating to the project's root folder and running `pip install -r requirements.txt`.
4. **This step should only be followed if you know what you're doing**. Add a line in your shell's rcfile saying `alias caesium="%PATH_TO_PROJECT%/caesium.py"` and replace `%PATH_TO_PROJECT%` with the absolute path to the project's root folder. You should now be able to start the prompt by running `caesium` from your shell.

## Usage

### Starting the Prompt

You can start the prompt by running `caesium`. Please note that this route only works if you followed Step 3 of the Installation guide.

You may also start it by running `python3 ./caesium.py` from the root directory of the project.

Example:

```
$ caesium
caesium v0.3.5 running on linux.
Press Ctrl+C to exit.
> 
```

### Values

There are only 2 builtin values: `True` and `False` (or `1` and `0`). The language is case-insensitive so you can write them however you want.

There is also the `random` keyword which randomly chooses to be either `True` or `False` every time it's used.

```
> TRUE
True
> False
False
> 0
True
> 1
False
> random
True
```

### Assignment

Assignment is done by putting a valid identifier on the left, a value or an expression on the right and putting a `=` between them. A valid identifier is any string of Unicode text that is not a keyword and that has no whitespace characters inside it. Assignments can be chained together. They can be nested within a more complex expression.

```
> foo = True
True
> quux = foo_bar = (True ^ (bar = True)) & False
False
```

### Operations

There are 4 main operators. These are:

1. `NOT`
2. `AND`
3. `OR`
4. `XOR`

`NOT` takes only one argument and negates it. `NOT` can also be written as `!`. This can be represented in a table as:

Value | Result
:---:|:---:|
`True` | `False`
`False` | `True`

`AND` takes 2 arguments and checks if both of them evaluate to `True`. If they both do, it returns `True`, otherwise it returns `False`. `AND` can also be written as `&` or `&&`. This can be represented in a table as:

Value 1 | Value 2 | Result
:---:|:---:|:---:|
`True` | `True` | `True`
`True` | `False` | `False`
`False` | `True` | `False`
`False` | `False` | `False`

`OR` also takes 2 arguments and checks if both of them evaluate to `False`. If they both do, it returns `False`, otherwise it returns `True`. `OR` can also be written as `|` or `||`. This can be represented in a table as:

Value 1 | Value 2 | Result
:---:|:---:|:---:|
`True` | `True` | `True`
`True` | `False` | `True`
`False` | `True` | `True`
`False` | `False` | `False`

`XOR` takes 2 arguments and checks if they evaluate to different values. If they do, it returns `True`, otherwise it returns `False`. `XOR` can also be written as `^`. This can be represented in a table as:

Value 1 | Value 2 | Result
:---:|:---:|:---:|
`True` | `True` | `False`
`True` | `False` | `True`
`False` | `True` | `True`
`False` | `False` | `False`

Expressions are evaluated right to left unless brackets (`()`) are used. If brackets are used, the innermost pair is evaluated going to the outermost. This also means that you can put an assignment in brackets then use its value in the same expression outside those brackets.

Examples:

```
> !False
True
> True XOR False
True
> False && 1
False
> !(((x = TRUE) ^ false) | x) && false
False
```

### Comments

Comments are lines of text meant for other people to read, rather than for the interpreter to run. If a line begins with a `#` character, the entire line is treated by the interpreter as if it is empty.

### Errors

As you may have noticed, when you try to run something wrong (like when there's a missing closing bracket), the interpreter throws an error. An error is basically the interpreter alerting you that there was something wrong with the expression so it couldn't run it successfully. Once an error is thrown, you will have to fix what your expression and rerun it.

Examples of errors:

```
> quux
Undefined name "quux".
> random/
Invalid syntax: "/".
```

### Closing the Prompt

Typing in `Control-C` at the prompt exits the interpreter. If that doesn't work, you can exit the interpreter by typing in `exit`. Using either route, the interpreter should print `Exiting...` then stop running.

```bash
> exit
Exiting...
$
```

## TODO

- [ ] Add a proper parse tree.
- [x] Add tests for the parts which use argparse.
- [ ] A standalone executable for those who don't want to install python.

## Development Setup

1. Create a virtualenv.
2. Install the development packages by running `pip install -r requirements-dev.txt`.
3. Assert everything is working by running  `pytest tests.py` from the project's root dir.

## Contributing

1. Fork the `develop` branch.
2. Create a branch for your feature.
3. Commit your changes.
4. Push to `origin`.
5. Create a pull request.

## Meta

- Name: **Armani Tallam**
- E-Mail: <armanitallam@gmail.com>
- Github: <https://www.github.com/Armani-T>

This project is available under the **BSD License**. See the [LICENSE.txt](./LICENSE.txt) file for more information.
