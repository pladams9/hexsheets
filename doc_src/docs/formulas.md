# Formulas

## Basic Syntax

Cell formulas start with an `=` character.

HexSheets currently recognizes three data types:

* `Strings` like `"abc"`
* `Integers` like `42`
* `Floats` like `3.14`

Four operands:

* Addition `+`
* Subtraction `-`
* Multiplication `*`
* Division `/`

And three types of brackets:

* String Quotes: `" "`
* Parentheses: `( )`
* Cell Addresses: `[ , ]`

## Order of Operations

HexSheets currently does not support basic order of operations. Parentheses are respected, but the basic operands are
calculated from left to right. This will likely change in future versions.

## Example formulas

* Not A Formula: `2 + 2` &rarr; `2 + 2`
* A Formula: `=2 + 2` &rarr; `4`
* No Parentheses: `=2 + 2 / 2` &rarr; `2`
* Parentheses: `=2 + (2 / 2)` &rarr; `3`
* String: `="Test" + 2` &rarr; `Test2`
* Cell Address: `=[3, 2]` &rarr; Value of Cell at [3, 2]
* Cell Address Evaluation: `=[1, (2 + 3)]` &rarr; Value of Cell at [1, 5]
