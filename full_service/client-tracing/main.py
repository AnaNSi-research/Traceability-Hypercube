from config import *
from client import Client

def menu():
    print("1- Deploy factory contract")
    print("2- Deploy new item")
    print("3- Search by keyword")
    print("4- Obtain item")
    print("0- Exit")
    choice = -1
    while choice < 0 or choice > 4:
        choice = int(input(f"\nInsert choice: "))

    return choice


if __name__ == '__main__':
    client = Client()

    while True:
        choice = menu()

        if choice == 1:
            pass #TODO
        elif choice == 2:
            pass #TODO
        elif choice == 3:
            pass #TODO
        elif choice == 4:
            pass #TODO

        if choice == 0:
            break

