from consolemenu import ConsoleMenu
from consolemenu.items import FunctionItem, SubmenuItem, CommandItem
from getpass import getpass

from .main_menu import main_menu


def login():
    username = input('username: ')
    password = getpass('password: ')

    # TODO: log into SQL server
    # Assuming success:
    main_menu.show()

    # TODO: open a different menu based on capabilities of user
    #       (online mode vs store mode)


def create_account():
    username = input('new username: ')
    # TODO: select from database to confirm username is available

    password = getpass('new password: ')
    while password != getpass('confirm password: '):
        print('\npasswords do not match - try again')
        password = getpass('new password: ')

    # TODO: create normal user account in SQL database

    input('\naccount created - press [enter] to continue to The Lego Store')

    main_menu.show()


# \/\/\/\/ LOGIN MENU \/\/\/\/

login_menu = ConsoleMenu('The Lego Store', 'Please log in to continue')

login_item = FunctionItem('Login', login)
create_account_item = FunctionItem('Create Account', create_account)

login_menu.append_item(login_item)
login_menu.append_item(create_account_item)