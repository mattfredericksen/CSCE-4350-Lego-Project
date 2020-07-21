from getpass import getpass

from consolemenu.screen import Screen

from menus.main_menu import main_menu
from menus.employee_main_menu import employee_main_menu


def login():
    username = input('username: ')

    # getpass doesn't show characters as user types
    password = getpass('password: ')

    # TODO: log into SQL server
    # Assuming success:
    if input("Are you an employee? (don't lie) [y/n]: ").lower() in ('yes', 'ye', 'y'):
        employee_main_menu.show()
    else:
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

    # TODO: get the rest of user account info

    # TODO: create normal user account in SQL database

    Screen.clear()
    input('Account created!\n\n'
          'Press [enter] to continue to The Lego Store.')

    main_menu.show()
