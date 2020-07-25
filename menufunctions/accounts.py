from getpass import getpass

from consolemenu.screen import Screen

from menus.main_menu import main_menu
from menus.employee_main_menu import employee_main_menu
from menus.customer_account_menu import change_store_preference

from sql import LegoDB


def login(database: LegoDB, store_mode: bool):
    username = input('Username: ')

    # getpass doesn't show characters as user types
    password = getpass('Password: ')

    if store_mode:
        if not database.employee_login(username, password):
            input('Incorrect username or password. Press [enter] to return.')
            return
    elif not database.customer_login(username, password):
        input('Incorrect username or password. Press [enter] to return.')
        return

    if store_mode:
        employee_main_menu(database)
    else:
        main_menu(database)


def create_account(database: LegoDB):
    print('CREATE ACCOUNT\n')

    username = input('New username: ')
    while database.username_exists(username):
        username = input('Username already taken.\n\nNew username: ')

    password = getpass('new password: ')
    while password != getpass('confirm password: '):
        print('\npasswords do not match - try again')
        password = getpass('new password: ')

    name = input('Name: ')
    email = input('Email: ')
    address = input('Address: ')

    try:
        database.create_customer(username, password, name, email, address, 1)
    except Exception as e:
        print(f'\n{e}')
        input('Failed to create new account. Press [enter] to return.')
    else:
        database.customer_login(username, password)
        change_store_preference(database)
        main_menu(database)
