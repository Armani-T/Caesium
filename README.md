# Caesium README

A simple language for running Boolean algebraic expressions. It is based on the idea that this language should be as compatible as possible with other languages. I built it to run my own Boolean expressions for prototyping complex if statements.

## Installation

1. Ensure that you have a working version of python 3 (If not, you can get it from the [official site](https://www.python.org)).
2. Just clone the repo using `git clone`.
3. Add `./Caesium/caesium.py` to your `PATH` so that you can start the prompt by running `caesium` (**This part is optional**).

## Usage

### Starting the Prompt

As of now, there are 2 ways to start the prompt:

- Running `./caesium.sh` from the project's root directory on a UNIX shell (e.g. `bash` or `fish`).
- Running `python caesium.py` from the project's root directory (which is what the other option does for you).

### Values

There are only 2 builtin values: `True` and `False`.
You can write them in full or as `1` and `0`.
The language is case-insensitive so you can write them in any way you want.

### Assignment

Assignments are expressions which evaluate to the variable's value.
They can be nested within another, more complex expression.
Variables can be assigned to both single values and the results of expressions.

### Operations

There are 4 main operators. These are:

- `NOT` or `!`
- `AND`, `&` or `&&`
- `OR`, `|` or `||`
- `XOR` or `^`

No operator has a higher binding power than another, expressions are evaluated right to left.
Parentheses (`()`) are used to group operations.
All operators except `NOT` are put between their arguments since they are binary.
`NOT` is a unary operator, it is put before its parameter.

### Errors

As you may have noticed, when you type in a wrong expression (like if a closing parenthesis is missing) the interpreter throws an error. An error is basically just an alert to tell you that there was something wrong with an expression. Once an error is thrown, you will have to fix what you entered and run it again. Unlike larger, fuller languages, there is no error catching or throwing mechanism in here.

### Closing the Prompt

Typing in `Control-C` at the prompt exits the interpreter. If that doesn't work, you can exit the interpreter by typing in `exit`. Using either route, the interpreter should print `Exiting...` then stop running.

```
Caesium v0.2.0 running on linux.
Press Ctrl+C to exit.
>> !True
False
>> false & TRUE
False
>> TRUE | False
True
>> False ^ (y = True)
True
>> x = !((True & False) | y) ^ False
False
>> exit
Exiting...
```

## Coming Soon

- A proper parse tree.
- Conditional expressions.

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

This project is available under the **BSD 3-Clause License**. See [LICENSE.txt](./LICENSE.txt) for more information.
