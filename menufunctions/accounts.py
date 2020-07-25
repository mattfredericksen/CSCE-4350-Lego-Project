from getpass import getpass

from consolemenu.screen import Screen

from menus.main_menu import main_menu
from menus.employee_main_menu import employee_main_menu
from sql import LegoDB


def login(store_mode: bool, database: LegoDB):
    username = input('Username: ')

    # getpass doesn't show characters as user types
    password = getpass('Password: ')

    if store_mode:
        # use employee table for checking username & password
        pass
    else:
        if not database.customer_login(username, password):
            input('Incorrect username or password. Press [enter] to return.')
            return

    # TODO: log into SQL server

    # Assuming success:
    if store_mode:
        # temporary:
        database.store = 1
        employee_main_menu(database)
    else:
        main_menu(database)


def create_account(database: LegoDB):
    username = input('New username: ')
    while database.username_exists(username):
        username = input('Username already taken.\n\nNew username: ')

    password = getpass('new password: ')
    while password != getpass('confirm password: '):
        print('\npasswords do not match - try again')
        password = getpass('new password: ')

    # TODO: get the rest of user account info
    #       create normal user account in SQL database

    Screen.clear()
    input('Account created! (not yet)\n\n'
          'Press [enter] to continue to The Lego Store.')

    database.customer_login(username, password)
    main_menu(database)
