# Caesium README

A simple "calc" for Boolean Algebra. It is based on the idea that this language should be as compatible as possible with other languages. The implementation provided is in python.

## Installation

1. Just clone the repo using `git clone`.

**This part is optional.**

2. Add `./Caesium/caesium.py` to your `PATH` so that you can start the prompt by running `caesium`.

## Usage

### Starting the Prompt

As of now there are 2 ways to start the Caesium prompt:
- Running `./caesium.sh` on `bash`  from the project's  root directory.
- Running `python caesium.py` from the project's  root directory.

### Values

There are only 2 builtin values: `True` and `False`.
You can write them in full or as `1` and `0`.
The language is case-insensitive so you can write them in any way you wish.

### Assignment

Assignments are expressions which evaluate to the variable's value.
They can be nested within another, more complex expression.
Variables can be assigned to both single values and the results of expressions.

### Operations

There are 4 main operators in Caesium. These are:

1. `NOT`: It can also be written as a `!`.
2. `AND`: It can also be written as `&` or `&&`.
3. `OR`:  It can also be written as `|` or `||`.
4. `XOR`: It can also be written as `^`.

No operator has a higher binding power than another, expressions are evaluated right to left.
Parentheses (`()`) are used to group operations.
All operators except `NOT` are put between their arguments since they are binary.
`NOT` is a unary operator, it is put before its parameter.

```
Caesium v0.1.2 running on win32.
Press Ctrl+C to exit.
>> !True
False
>> false & TRUE
False
>> True | False
True
>> False ^ (y = True)
True
>> x = !((True & False) | y) ^ False
False
>> 
Exiting...
```

## Coming Soon

- [] A proper parse tree (to get rid of some annoying errors).
- [] A better exit mechanism (preferrably as a function).
- [] Conditional expressions.

## Contributing

1. Fork the `develop` branch.
2. Create a branch for your feature.
3. Commit your changes.
4. Push to `origin`.
4. Create a pull request.

## Meta

- Name: **Armani Tallam**
- E-Mail: <armanitallam@gmail.com>
- Github: <https://www.github.com/Armani-T/>

This project is available under the **BSD 3-Clause License**. See [LICENSE.txt](./LICENSE.txt) for more information/
