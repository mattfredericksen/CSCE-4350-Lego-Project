from getpass import getpass

from consolemenu.screen import Screen

from menus.main_menu import main_menu
from menus.employee_main_menu import employee_main_menu


def login(store_mode: bool):
    username = input('username: ')

    # getpass doesn't show characters as user types
    password = getpass('password: ')

    if store_mode:
        # use employee table for checking username & password
        pass
    else:
        # use customer table ...
        pass

    # TODO: log into SQL server
    #       store credentials in `context` dict

    context = {'username': username,
               'password': password}

    # Assuming success:
    if store_mode:
        # temporary:
        context['store'] = int(input('Store ID: '))
        employee_main_menu(context)
    else:
        main_menu(context)

    # TODO: open a different menu based on capabilities of user
    #       (online mode vs store mode)


def create_account():
    username = input('new username: ')
    # TODO: select from database to confirm username is available

    password = getpass('new password: ')
    while password != getpass('confirm password: '):
        print('\npasswords do not match - try again')
        password = getpass('new password: ')

    # TODO: get the rest of user account info
    #       create normal user account in SQL database
    #       store credentials in context
    context = {'username': username,
               'password': password}

    Screen.clear()
    input('Account created!\n\n'
          'Press [enter] to continue to The Lego Store.')

    main_menu(context)
