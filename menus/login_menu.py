"""This is the first menu opened upon launching the application."""

from consolemenu import ConsoleMenu
from consolemenu.items import FunctionItem

from menufunctions.accounts import login, create_account


login_menu = ConsoleMenu('The Lego Store', 'Please log in to continue')

for item in (FunctionItem('Login', login),
             FunctionItem('Create Account', create_account)):
    login_menu.append_item(item)
