from config import *
from keywords import Brand, Colour
from client import Client
from web3 import Web3
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator
from InquirerPy.validator import PathValidator


def choices_from_enum(enum):
    return [Choice(name=str(e.name).capitalize(), value=e) for e in enum]


def get_brand():
    choices = choices_from_enum(Brand)
    return inquirer.select(
        message="Select a brand:",
        choices=choices,
    ).execute()


def get_colour():
    choices = choices_from_enum(Colour)
    return inquirer.select(
        message="Select a colour:",
        choices=choices,
    ).execute()


def menu(attached_factory: bool):
    choices = [
        Separator(line="*** Factory contract ***"),
        Choice(name="Deploy new factory contract", value="df"),
        Choice(name="Attach an existing factory contract", value="af")
    ]
    if attached_factory:
        choices += [
            Separator(line="*** Insertion ***"),
            Choice(name="Deploy new car", value="dc"),
            Separator(line="*** Search ***"),
            Choice(name="Get car", value="gc"),
            Choice(name="Pin-Search by keyword", value="pk"),
            Choice(name="Superset-Search by keyword", value="sk"),
        ]
    choices += [
        Separator(line=""),
        Choice(name="Exit", value="ex"),
    ]

    choice = inquirer.select(
        message="Select an action:",
        choices=choices,
    ).execute()

    return choice


if __name__ == '__main__':
    attached_factory = False
    while True:
        choice = menu(attached_factory)

        if choice == "df":
            f_choice = inquirer.select(
                message="Select the kind of factory to deploy:",
                choices=[
                    Choice(name="Standard", value="s"),
                    Choice(name="Clone", value="c")
                ],
            ).execute()
            if f_choice == "s":
                # TODO
                pass
            elif f_choice == "c":
                # TODO
                pass

            attached_factory = True
            # TODO deploy factory
        elif choice == "af":
            address = inquirer.text(message="Enter car factory address:",
                                    validate=Web3.is_address, invalid_message="Invalid contract address").execute()
            attached_factory = True
            # TODO attach factory
        elif choice == "dc":
            brand = get_brand()
            colour = get_colour()
            img_path = inquirer.filepath(
                message="Enter car image file path:",
                default="./objects/",
                validate=PathValidator(
                    is_file=True, message="Input is not a file"),
                only_files=True,
            ).execute()
            # TODO deploy car
        elif choice == "gc":
            address = inquirer.text(message="Enter car address:", validate=Web3.is_address,
                                    invalid_message="Invalid contract address").execute()
            pass  # TODO # get car
        elif choice == "pk":
            brand = get_brand()
            colour = get_colour()
            # TODO # pin search
        elif choice == "sk":
            k_choice = inquirer.select(
                message="Select the keyword by which perform the search:",
                choices=[
                    Choice(name="Brand", value="b"),
                    Choice(name="Colour", value="c")
                ],
            ).execute()
            if k_choice == "b":
                brand = get_brand()
                colour = None
            elif k_choice == "c":
                colour = get_colour()
                brand = None
            # TODO # superset search
        elif choice == "ex":
            print("Bye")
            break

        print()
