"""This is the menu that employees see upon logging in."""

from consolemenu import ConsoleMenu
from consolemenu.items import FunctionItem

from menuclasses.not_implemented_item import NotImplementedItem
from .sale_menu import sale_menu
from .store_menu import store_menu
from .employee_menu import employee_menu


def employee_main_menu(context: dict):
    menu = ConsoleMenu('Welcome, working-class scum',
                       exit_option_text='Log Out')

    for item in (FunctionItem('Start a Sale', sale_menu, (context,)),
                 NotImplementedItem('Start a Return'),
                 NotImplementedItem('Inventory Management'),  # order/delivery
                 FunctionItem('Employee Management', employee_menu, (context,)),
                 FunctionItem('Store Management', store_menu, (context,)),
                 NotImplementedItem('Reports')):

        menu.append_item(item)
    menu.show()

    # if employee is a manager, add more menu options
