"""This is the first menu opened upon launching the application."""

from consolemenu import ConsoleMenu
from consolemenu.items import FunctionItem

from menufunctions.accounts import login, create_account


def login_menu(database):
    menu = ConsoleMenu('The Lego Store', 'Please log in to continue')

    for item in (FunctionItem('Customer Login', login, [database, False]),
                 FunctionItem('Create Account', create_account, [database]),
                 FunctionItem('Store Mode', login, [database, True])):
        menu.append_item(item)
    menu.show()
