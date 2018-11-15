# CUTIE

*Commandline User Tools for Input Easification*

[![PRs Welcome](https://img.shields.io/badge/Homepage-GitHub-green.svg)](https://github.com/kamik423/cutie)
[![PyPI version](https://badge.fury.io/py/cutie.svg)](https://badge.fury.io/py/cutie)
[![PyPI license](https://img.shields.io/pypi/l/cutie.svg)](https://pypi.python.org/pypi/cutie/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/cutie.svg)](https://pypi.python.org/pypi/cutie/)
[![PEP8](https://img.shields.io/badge/code%20style-pep8-orange.svg)](https://www.python.org/dev/peps/pep-0008/)

A tool for handling common user input functions in an elegant way.
It supports asking yes or no questions, selecting an element from a list with arrow keys, forcing the user to input a number and secure text entry while having many customization options.

For example the yes or no input supports forcing the user to match case, tab autocomplete and switching option with the arrow keys.
The number input allows setting a minum and a maximum, entering floats or forcing the user to use integers.
It will only return once the user inputs a number in that format, showing a warning to them if it does not conform.

It should work on all major operating systems (Mac, Linux, Windows).

![example](https://github.com/Kamik423/cutie/blob/master/example.gif?raw=true)

## Usage

These are the main functions of cutie:

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

```bash
pip3 install cutie
```

## Documentation

### get\_number

Get a number from user input.
If an invalid number is entered the user will be prompted again.

#### Arguments

| argument    | type            | default    | description                          |
|:------------|:----------------|:-----------|:-------------------------------------|
| prompt      | str             |            | The prompt asking the user to input. |
| min_value   | float, optional | - infinity | The [inclusive] minimum value.       |
| max_value   | float, optional | infinity   | The [inclusive] maximum value.       |
| allow_float | bool, optional  | True       | Allow floats or force integers.      |

#### Returns

The number input by the user.

### secure\_input

Get secure input without showing it in the command line.

#### Arguments

| argument | type | description                          |
|:---------|:-----|:-------------------------------------|
| prompt   | str  | The prompt asking the user to input. |

#### Returns

The secure input.

### select

Select an option from a list.

#### Arguments

| argument          | type                | default | description                        |
|:------------------|:--------------------|:--------|:-----------------------------------|
| options           | List[str]           |         | The options to select from.        |
| caption_indices   | List[int], optional | `None`  | Non-selectable indices.            |
| deselected_prefix | str, optional       | `[ ]`   | Prefix for deselected option.      |
| selected_prefix   | str, optional       | `[x]`   | Prefix for selected option.        |
| caption_prefix    | str, optional       | ``      | Prefix for captions.               |
| selected_index    | int, optional       | 0       | The index to be selected at first. |

#### Returns

The index that has been selected.

### prompt\_yes\_or\_no

Prompt the user to input yes or no.

#### Arguments

| argument             | type                     | default | description                          |
|:---------------------|:-------------------------|:--------|:-------------------------------------|
| question             | str                      |         | The prompt asking the user to input. |
| yes_text             | str, optional            | `Yes`   | The text corresponding to 'yes'.     |
| no_text              | str, optional            | `No`    | The text corresponding to 'no'.      |
| has_to_match_case    | bool, optional           | `False` | Does the case have to match.         |
| enter_empty_confirms | bool, optional           | True    | Does enter on empty string work.     |
| default_is_yes       | bool, optional           | False   | Is yes selected by default           |
| deselected_prefix    | str, optional            | `  `    | Prefix if something is deselected.   |
| selected_prefix      | str, optional            | `> `    | Prefix if something is selected      |
| abort_value          | Optional[bool], optional | `None`  | The value on interrupt.              |
| char_prompt          | bool, optional           | `True`  | Add a [Y/N] to the prompt.           |

#### Returns

The bool what has been selected.

## Contributing

If you want to contribute, please feel free to suggest features or implement them yourself.

Also **please report any issues and bugs you might find!**

## Authors

* Main project by [me](https://github.com/Kamik423).
* Windows support by [Lhitrom](https://github.com/Lhitrom).
* `caption_indices` and tidbits by [dherrada](https://github.com/dherrada).

## License

The project is licensed under the [MIT-License](https://github.com/Kamik423/cutie/blob/master/license.md).

## Acknowledgments

* This project uses the module [Readchar](https://pypi.org/project/readchar/) for direct input handling.

---

*GNU Terry Pratchett*
