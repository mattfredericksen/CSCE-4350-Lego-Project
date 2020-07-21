"""This is the menu that employees see upon logging in."""

from consolemenu import ConsoleMenu
from consolemenu.items import FunctionItem

from menuclasses.not_implemented_item import NotImplementedItem
from menufunctions.sale import sale


def employee_main_menu(context: dict):
    menu = ConsoleMenu('Welcome, working-class scum',
                       exit_option_text='Log Out')

    for item in (FunctionItem('Start a Sale', sale, (context,)),
                 NotImplementedItem('Start a Return'),
                 NotImplementedItem('Order Management'),
                 NotImplementedItem('Delivery Management')):
        menu.append_item(item)
    menu.show()

    # if employee is a manager, add more menu options
