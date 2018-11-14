#! /usr/bin/env python3
"""cutie: Commandline User Tools for Input Easification
"""

import getpass
from typing import List, Optional

from colorama import init
import readchar


init()


def get_number(
        prompt: str,
        min_value: Optional[float] = None,
        max_value: Optional[float] = None,
        allow_float: bool = True) -> float:
    """Get a number from user input.
    If an invalid number is entered the user will be prompted again.

    Args:
        prompt (str): The prompt asking the user to input.
        min_value (float, optional): The [inclusive] minimum value.
        max_value (float, optional): The [inclusive] maximum value.
        allow_float (bool, optional): Allow floats or force integers.

    Returns:
        float: The number input by the user.
    """
    return_value: Optional[float] = None
    while return_value is None:
        input_value = input(prompt + ' ')
        try:
            return_value = float(input_value)
        except ValueError:
            print('Not a valid number.\033[K\033[1A\r\033[K', end='')
        if not allow_float and return_value is not None:
            if return_value != int(return_value):
                print('Has to be an integer.\033[K\033[1A\r\033[K', end='')
                return_value = None
        if min_value is not None and return_value is not None:
            if return_value < min_value:
                print(f'Has to be at least {min_value}.\033[K\033[1A\r\033[K',
                      end='')
                return_value = None
        if max_value is not None and return_value is not None:
            if return_value > max_value:
                print(f'Has to be at most {max_value}.\033[1A\r\033[K', end='')
                return_value = None
        if return_value is not None:
            break
    print('\033[K', end='')
    if allow_float:
        return return_value
    return int(return_value)


def secure_input(prompt: str) -> str:
    """Get secure input without showing it in the command line.

    Args:
        prompt (str): The prompt asking the user to input.

    Returns:
        str: The secure input.
    """
    return getpass.getpass(prompt + ' ')


def select(
        options: List[str],
        text: List[str],
        deselected_prefix: str = '\033[1m[ ]\033[0m ',
        selected_prefix: str = '\033[1m[\033[32;1mx\033[0;1m]\033[0m ',
        selected_index: int = 0) -> int:
    """Select an option from a list.

    Args:
        options (List[str]): The options to select from.
        deselected_prefix (str, optional): Prefix for deselected option ([ ]).
        selected_prefix (str, optional): Prefix for selected option ([x]).
        selected_index (int, optional): The index to be selected at first.

    Returns:
        int: The index that has been selected.
    """
    print('\n' * (len(options) - 1))
    while 1:
        print(f'\033[{len(options) + 1}A')
        for i, option in enumerate(options):
            if i not in text:
                print('\033[K{}{}'.format(
                    selected_prefix if i == selected_index else deselected_prefix,
                    option))
            elif i in text:
                print(options[i])
        keypress = readchar.readkey()
        if keypress == readchar.key.UP:
            if selected_index - 1 not in text:
                selected_index = max(selected_index - 1, 0)
            else:
                selected_index = max(selected_index - 2, 0)
        elif keypress == readchar.key.DOWN:
            if selected_index + 1 not in text:
                selected_index = min(selected_index + 1, len(options) - 1)
            else:
                selected_index = min(selected_index + 2, len(options) - 1)
        else:
            break
    return selected_index


def prompt_yes_or_no(
        question: str,
        yes_text: str = 'Yes',
        no_text: str = 'No',
        has_to_match_case: bool = False,
        enter_empty_confirms: bool = True,
        default_is_yes: bool = False,
        deselected_prefix: str = '  ',
        selected_prefix: str = '\033[31m>\033[0m ',
        abort_value: Optional[bool] = None,
        char_prompt: bool = True) -> Optional[bool]:
    """Prompt the user to input yes or no.

    Args:
        question (str): The prompt asking the user to input.
        yes_text (str, optional): The text corresponding to 'yes'.
        no_text (str, optional): The text corresponding to 'no'.
        has_to_match_case (bool, optional): Does the case have to match.
        enter_empty_confirms (bool, optional): Does enter on empty string work.
        default_is_yes (bool, optional): Is yes selected by default (no).
        deselected_prefix (str, optional): Prefix if something is deselected.
        selected_prefix (str, optional): Prefix if something is selected (> )
        abort_value (Optional[bool], optional): The value on interrupt.
        char_prompt (bool, optional): Add a [Y/N] to the prompt.

    Returns:
        Optional[bool]: The bool what has been selected.
    """
    is_yes = default_is_yes
    is_selected = enter_empty_confirms
    current_message = ''
    yn_prompt = f' ({yes_text[0]}/{no_text[0]}) ' if char_prompt else ': '
    abort = False
    print()
    while 1:
        yes = is_yes and is_selected
        no = not is_yes and is_selected
        print('\033[K'
              f'{selected_prefix if yes else deselected_prefix}{yes_text}')
        print('\033[K'
              f'{selected_prefix if no else deselected_prefix}{no_text}')
        print('\033[3A\r\033[K'
              f'{question}{yn_prompt}{current_message}', end='', flush=True)
        keypress = readchar.readkey()
        if keypress in [readchar.key.DOWN, readchar.key.UP]:
            is_yes = not is_yes
            is_selected = True
            current_message = yes_text if is_yes else no_text
        elif keypress in [readchar.key.BACKSPACE, readchar.key.LEFT]:
            if current_message:
                current_message = current_message[:-1]
        elif keypress in [readchar.key.CTRL_C, readchar.key.CTRL_D]:
            abort = True
            break
        elif keypress in [readchar.key.ENTER, readchar.key.RIGHT]:
            if is_selected:
                break
        elif keypress in '\t':
            if is_selected:
                current_message = yes_text if is_yes else no_text
        else:
            current_message += keypress
            match_yes = yes_text
            match_no = no_text
            match_text = current_message
            if not has_to_match_case:
                match_yes = match_yes.upper()
                match_no = match_no.upper()
                match_text = match_text.upper()
            if match_no.startswith(match_text):
                is_selected = True
                is_yes = False
            elif match_yes.startswith(match_text):
                is_selected = True
                is_yes = True
            else:
                is_selected = False
        print()
    print('\033[K\n\033[K\n\033[K\n\033[3A')
    if abort:
        return abort_value
    return is_selected and is_yes
