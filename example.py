#! /usr/bin/env python3
"""Example script demonstrating usage of cutie.
"""

import cutie


def main():
    """Main."""
    if cutie.prompt_yes_or_no("Are you brave enough to continue?"):
        # List of names to select from, including some captions
        names = [
            "Kings:",
            "Arthur, King of the Britons",
            "Knights of the Round Table:",
            "Sir Lancelot the Brave",
            "Sir Robin the Not-Quite-So-Brave-as-Sir-Lancelot",
            "Sir Bedevere the Wise",
            "Sir Galahad the Pure",
            "Swedish captions:",
            "Møøse",
        ]
        # Names which are captions and thus not selectable
        captions = [0, 2, 7]
        # Get the name
        name = names[cutie.select(names, caption_indices=captions, selected_index=8)]
        print(f"Welcome, {name}")
        # Get an integer greater or equal to 0
        age = cutie.get_number("What is your age?", min_value=0, allow_float=False)
        nemeses_options = [
            "The French",
            "The Police",
            "The Knights Who Say Ni",
            "Women",
            "The Black Knight",
            "The Bridge Keeper",
            "Especially terrifying:",
            "The Rabbit of Caerbannog",
        ]
        print("Choose your nemeses")
        # Choose multiple options from a list
        nemeses_indices = cutie.select_multiple(
            nemeses_options, caption_indices=[6], hide_confirm=False
        )
        nemeses = [
            nemesis
            for nemesis_index, nemesis in enumerate(nemeses_options)
            if nemesis_index in nemeses_indices
        ]
        # Get input without showing it being typed
        quest = cutie.secure_input("What is your quest?")
        print(f"{name}'s quest (who is {age}) is {quest}.")
        if nemeses:
            if len(nemeses) == 1:
                print(f"His nemesis is {nemeses[0]}.")
            else:
                print(f'His nemeses are {" and ".join(nemeses)}.')
        else:
            print("He has no nemesis.")


if __name__ == "__main__":
    main()
