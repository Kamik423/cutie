# CUTIE

*Command line User Tools for Input Easification*

[![Build Status](https://travis-ci.org/Kamik423/cutie.svg?branch=master)](https://travis-ci.org/Kamik423/cutie)
[![Coverage Status](https://coveralls.io/repos/github/Kamik423/cutie/badge.svg?branch=coveralls_integration)](https://coveralls.io/github/Kamik423/cutie?branch=coveralls_integration)
[![PRs Welcome](https://img.shields.io/badge/Homepage-GitHub-green.svg)](https://github.com/kamik423/cutie)
[![PyPI version](https://badge.fury.io/py/cutie.svg)](https://badge.fury.io/py/cutie)
[![PyPI license](https://img.shields.io/pypi/l/cutie.svg)](https://pypi.python.org/pypi/cutie/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/cutie.svg)](https://pypi.python.org/pypi/cutie/)
[![PEP8](https://img.shields.io/badge/code%20style-pep8-orange.svg)](https://www.python.org/dev/peps/pep-0008/)
[![GitHub contributors](https://img.shields.io/github/contributors/Kamik423/cutie.svg)](https://GitHub.com/Kamik423/cutie/graphs/contributors/)

A tool for handling common user input functions in an elegant way.
It supports asking yes or no questions, selecting an element from a list with arrow keys or vim arrow keys, forcing the user to input a number and secure text entry while having many customization options.

For example the yes or no input supports forcing the user to match case, tab autocomplete and switching option with the arrow keys.
The number input allows setting a minum and a maximum, entering floats or forcing the user to use integers.
It will only return once the user inputs a number in that format, showing a warning to them if it does not conform.

It should work on all major operating systems (Mac, Linux, Windows).

![example](https://github.com/Kamik423/cutie/blob/master/example.gif?raw=true)

## Usage

These are the main functions of cutie.
[example.py](https://github.com/Kamik423/cutie/blob/master/example.py) contains an extended version of this also showing off the `select_multiple` option.

```python
import cutie

if cutie.prompt_yes_or_no('Are you brave enough to continue?'):
    # List of names to select from, including some captions
    names = [
        'Kings:',
        'Arthur, King of the Britons',
        'Knights of the Round Table:',
        'Sir Lancelot the Brave',
        'Sir Robin the Not-Quite-So-Brave-as-Sir-Lancelot',
        'Sir Bedevere the Wise',
        'Sir Galahad the Pure',
        'Swedish captions:',
        'Møøse']
    # Names which are captions and thus not selectable
    captions = [0, 2, 7]
    # Get the name
    name = names[
        cutie.select(names, caption_indices=captions, selected_index=8)]
    print(f'Welcome, {name}')
    # Get an integer greater or equal to 0
    age = cutie.get_number(
        'What is your age?',
        min_value=0,
        allow_float=False)
    # Get input without showing it being typed
    quest = cutie.secure_input('What is your quest?')
    print(f'{name}\'s quest (who is {age}) is {quest}.')
```

When run, as demonstrated in the gif above it yields this output:

```
Are you brave enough to continue? (Y/N) Yes
Kings:
[ ] Arthur, King of the Britons
Knights of the Round Table:
[ ] Sir Lancelot the Brave
[x] Sir Robin the Not-Quite-So-Brave-as-Sir-Lancelot
[ ] Sir Bedevere the Wise
[ ] Sir Galahad the Pure
Swedish captions:
[ ] Møøse
Welcome, Sir Robin the Not-Quite-So-Brave-as-Sir-Lancelot
What is your age? 31
What is your quest?
Sir Robin the Not-Quite-So-Brave-as-Sir-Lancelot's quest (who is 31) is to find the holy grail.
```

## Installation

With pip from pypi:

```bash
pip3 install cutie
```

With pip from source or in a virtual environment:

```bash
pip3 install -r requirements.txt
```

## Documentation

All functions of cutie are explained here.
If something is still unclear or you have questions about the implementation just take a look at [cutie.py](https://github.com/Kamik423/cutie/blob/master/cutie.py).
The implementation is rather straight forward.

### get\_number

Get a number from user input.

If an invalid number is entered the user will be prompted again.
A minimum and maximum value can be supplied. They are inclusive.
If the `allow_float` option, which is `True` by default is set to `False` it forces the user to enter an integer.

Getting any three digit number for example could be done like that:

```python
number = cutie.get_number(
    'Please enter a three digit number:',
    min_value=100,
    max_value=999,
    allow_float=False)
# which is equivalent to
number = cutie.get_number('Please enter a three digit number', 100, 999, False)
```

#### Arguments

| argument      | type            | default    | description                          |
|:--------------|:----------------|:-----------|:-------------------------------------|
| `prompt`      | str             |            | The prompt asking the user to input. |
| `min_value`   | float, optional | - infinity | The [inclusive] minimum value.       |
| `max_value`   | float, optional | infinity   | The [inclusive] maximum value.       |
| `allow_float` | bool, optional  | True       | Allow floats or force integers.      |

#### Returns

The number input by the user.

### secure\_input

Get secure input without showing it in the command line.

This could be used for passwords:

```python
password = cutie.secure_input('Please enter your password:')
```

#### Arguments

| argument | type | description                          |
|:---------|:-----|:-------------------------------------|
| `prompt` | str  | The prompt asking the user to input. |

#### Returns

The secure input.

### select

Select an option from a list.

Captions or separators can be included between options by adding them as an option and including their index in `caption_indices`.
A preselected index can be supplied.

In its simplest case it could be used like this:

```python
colors = ['red', 'green', 'blue', 'yellow']
print('What is your favorite color?')
favorite_color = colors[cutie.select(colors)]
```

With the high degree of customizability, however it is possible to do things like:

```python
print('Select server to ping')
server_id = cutie.select(
    servers,
    deselected_prefix='    ',
    selected_prefix='PING',
    selected_index=default_server_ip)
```

#### Arguments

| argument            | type                | default | description                        |
|:--------------------|:--------------------|:--------|:-----------------------------------|
| `options`           | List[str]           |         | The options to select from.        |
| `caption_indices`   | List[int], optional | `None`  | Non-selectable indices.            |
| `deselected_prefix` | str, optional       | `[ ]`   | Prefix for deselected option.      |
| `selected_prefix`   | str, optional       | `[x]`   | Prefix for selected option.        |
| `caption_prefix`    | str, optional       | ` `     | Prefix for captions.               |
| `selected_index`    | int, optional       | 0       | The index to be selected at first. |
| `confirm_on_select` | bool, optional      | True    | Select keys also confirm.          |

#### Returns

The index that has been selected.

### select\_multiple

Select multiple options from a list.

It per default shows a "confirm" button.
In that case space bar and enter select a line.
The button can be hidden.
In that case space bar selects the line and enter confirms the selection.

This is not in the example in this readme, but in [example.py](https://github.com/Kamik423/cutie/blob/master/example.py).

```python
packages_to_update = cutie.select_multiple(
    outdated_packages,
    deselected_unticked_prefix='  KEEP  ',
    deselected_ticked_prefix=' UPDATE ',
    selected_unticked_prefix='[ KEEP ]',
    selected_ticked_prefix='[UPDATE]',
    ticked_indices=list(range(len(outdated_packages))),
    deselected_confirm_label='  [[[[ UPDATE ]]]]  ',
    selected_confirm_label='[ [[[[ UPDATE ]]]] ]')
```

#### Arguments

| argument                     | type                | default         | description                                                                                                |
|:-----------------------------|:--------------------|:----------------|:-----------------------------------------------------------------------------------------------------------|
| `options`                    | List[str]           |                 | The options to select from.                                                                                |
| `caption_indices`            | List[int], optional |                 | Non-selectable indices.                                                                                    |
| `deselected_unticked_prefix` | str, optional       | `( )`           | Prefix for lines that are not selected and not ticked .                                                    |
| `deselected_ticked_prefix`   | str, optional       | `(x)`           | Prefix for lines that are not selected but ticked .                                                        |
| `selected_unticked_prefix`   | str, optional       | `{ }`           | Prefix for lines that are selected but not ticked .                                                        |
| `selected_ticked_prefix`     | str, optional       | `{x}`           | Prefix for lines that are selected and ticked .                                                            |
| `caption_prefix`             | str, optional       | ` `             | Prefix for captions.                                                                                       |
| `ticked_indices`             | List[int], optional | `[]`            | Indices that are ticked initially.                                                                         |
| `cursor_index`               | int, optional       | 0               | The index the cursor starts at.                                                                            |
| `minimal_count`              | int, optional       | 0               | The minimal amount of lines that have to be ticked.                                                        |
| `maximal_count`              | int, optional       | infinity        | The maximal amount of lines that have to be ticked.                                                        |
| `hide_confirm`               | bool, optional      | `False`         | Hide the confirm button. This causes `<ENTER>` to confirm the entire selection and not just tick the line. |
| `deselected_confirm_label`   | str, optional       | `(( confirm ))` | The confirm label if not selected.                                                                         |
| `selected_confirm_label`     | str, optional       | `{{ confirm }}` | The confirm label if selected.                                                                             |

#### Returns

A list of indices that have been selected.

### prompt\_yes\_or\_no

Prompt the user to input yes or no.

This again can range from very simple to very highly customized:

```python
if cutie.prompt_yes_or_no('Do you want to continue?'):
    do_continue()
```

```python
if cutie.prompt_yes_or_no(
    'Do you want to hear ze funniest joke in ze world? Proceed at your own risk.',
    yes_text='JA',
    no_text='nein',
    has_to_match_case=True, # The user has to type the exact case
    enter_empty_confirms=False, # An answer has to be selected
    )
```

#### Arguments

| argument               | type           | default | description                          |
|:-----------------------|:---------------|:--------|:-------------------------------------|
| `question`             | str            |         | The prompt asking the user to input. |
| `yes_text`             | str, optional  | `Yes`   | The text corresponding to 'yes'.     |
| `no_text`              | str, optional  | `No`    | The text corresponding to 'no'.      |
| `has_to_match_case`    | bool, optional | `False` | Does the case have to match.         |
| `enter_empty_confirms` | bool, optional | True    | Does enter on empty string work.     |
| `default_is_yes`       | bool, optional | False   | Is yes selected by default           |
| `deselected_prefix`    | str, optional  | `  `    | Prefix if something is deselected.   |
| `selected_prefix`      | str, optional  | `> `    | Prefix if something is selected      |
| `char_prompt`          | bool, optional | `True`  | Add a [Y/N] to the prompt.           |

#### Returns

The bool what has been selected.

## Changelog

### [dev]

* Unittests by [provinzkraut](https://github.com/provinzkraut)
* Travis CI integration
* Vim Arrow keys (`jk`)
* Also showing error messages with `hide_confirm` option enabled in `select_multiple`
* Consistenly crash on keyboard interrupt (Removes `prompt_yes_or_no`'s `abort_value`)

### 0.2.2

* Fixed Python in examples
* PEP8 Compliance by [Christopher Bilger](https://github.com/ChristopherBilg)
* Fixed critical issue with pypi download ([#15](https://github.com/Kamik423/cutie/issues/15))

### 0.2.1

* Expanded readme descriptions

### 0.2.0

* `select_multiple`
* Tweaks to the readme

### 0.1.1

* Fixed pypi download not working

### 0.1.0

* `caption_indices` option by [dherrada](https://github.com/dherrada)

### 0.0.7

* Windows support by [Lhitrom](https://github.com/Lhitrom)

### 0.0.x

* Initial upload and got everything working


## Contributing

If you want to contribute, please feel free to suggest features or implement them yourself.

Also **please report any issues and bugs you might find!**

If you have a project that uses cutie please let me know and I'll link it here!

## Authors

* Main project by [me](https://github.com/Kamik423).
* Unittests, issues and advice by [provinzkraut](https://github.com/provinzkraut).
* Windows support by [Lhitrom](https://github.com/Lhitrom).
* `caption_indices` and tidbits by [dherrada](https://github.com/dherrada).
* PEP8 Compliance by [Christopher Bilger](https://github.com/ChristopherBilg).

## License

The project is licensed under the [MIT-License](https://github.com/Kamik423/cutie/blob/master/license.md).

## Acknowledgments

* This project uses the module [Readchar](https://pypi.org/project/readchar/) for direct input handling.

---

*GNU Terry Pratchett*
