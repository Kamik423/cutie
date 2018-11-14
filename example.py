#! /usr/bin/env python3
"""Example script demonstrating usage of cutie.
"""

import cutie


def main():
    """Main.
    """
    if cutie.prompt_yes_or_no('Are you brave enough to continue?'):
        names = [
            'Arthur, King of the Britons',
            'Sir Lancelot the Brave',
            'Sir Robin the Not-Quite-So-Brave-as-Sir-Lancelot',
            'Sir Bedevere the Wise',
            'Sir Galahad the Pure',
            'Møøse']
        name = names[cutie.select(names, selected_index=5)]
        print(f'Welcome, {name}')
        age = cutie.get_number(
            'What is your age?',
            min_value=0,
            allow_float=False)
        quest = cutie.secure_input('What is your quest?')
        print(f'{name}\'s quest (who is {age}) is {quest}.')


if __name__ == '__main__':
    main()
