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
            Separator(line="*** Data management ***"),
            Choice(name="Create new car", value="dc"),
            Choice(name="Remove car from hypercube", value="rc"),
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
    client = Client()
    print()

    attached_factory = False
    while True:
        choice = menu(attached_factory)

        if choice == "df": # deploy factory
            f_choice = inquirer.select(
                message="Select the kind of factory to deploy:",
                choices=[
                    Choice(name="Standard", value="s"),
                    Choice(name="Clone", value="c")
                ],
            ).execute()
            if f_choice == "s": # standard factory
                tx_receipt = client.deploy_standard_factory()
            elif f_choice == "c": #clone factory
                tx_receipt, tx_receipt_base_car = client.deploy_clone_factory()
                print("Total gas used:", (tx_receipt_base_car.gasUsed + tx_receipt.gasUsed))
                print("Gas to deploy base car:", tx_receipt_base_car.gasUsed)

            print("Gas to deploy factory:", tx_receipt.gasUsed)
            print("Factory deployed at", tx_receipt.contractAddress)

            attached_factory = True
        elif choice == "af": # attach factory
            address = inquirer.text(message="Enter car factory address:",
                                    validate=Web3.is_address, invalid_message="Invalid contract address").execute()
            facotry_path = inquirer.filepath(
                message="Enter solidity factory code file path:",
                default="./contracts/",
                validate=PathValidator(
                    is_file=True, message="Input is not a file"),
                only_files=True,
            ).execute()
            facotry_name = inquirer.text(message="Enter factory contract name:").execute()

            # TODO compile and attach factory

            attached_factory = True
        elif choice == "dc": # deploy car
            brand = get_brand()
            colour = get_colour()
            img_path = inquirer.filepath(
                message="Enter car image file path:",
                default="./objects/",
                validate=PathValidator(
                    is_file=True, message="Input is not a file"),
                only_files=True,
            ).execute()

            keyword, tx_receipt, hypercube_res = client.create_car(brand, colour, img_path)
        elif choice == "rc": # remove car
            address = inquirer.text(message="Enter car address:", validate=Web3.is_address,
                                    invalid_message="Invalid contract address").execute()
            brand = get_brand()
            colour = get_colour()
            
            res = client.remove_car(address, brand, colour)
            print("Rmove car", address, "outcome", res)
        elif choice == "gc": # get car
            address = inquirer.text(message="Enter car address:", validate=Web3.is_address,
                                    invalid_message="Invalid contract address").execute()
            brand, colour, owner, ipfs_img = client.car_info(address)

            print("Brand:", brand.name.capitalize())
            print("Clour:", colour.name.capitalize())
            print("Owner:", owner)
            print("IPFS img:", ipfs_img)
        elif choice == "pk": # pin search
            brand = get_brand()
            colour = get_colour()
            
            keyword, res = client.search_car(brand, colour)

            objects = res.text.strip().split(",")
            print("{} Objects with keyword {}:".format(len(objects), keyword))
            for o in objects:
                print(o)
        elif choice == "sk": # superset search
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
            
            keyword, res = client.superset_search(brand, colour)

            objects = res.text.strip().split(",")
            print("{} Objects at distance [0, 1] with keyword {}:".format(len(objects), keyword))
            for o in objects:
                print(o)
        elif choice == "ex":
            print("Bye")
            break

        print()
