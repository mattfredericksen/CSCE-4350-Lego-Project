"""This is the menu that employees see upon logging in."""

from consolemenu import ConsoleMenu
from consolemenu.items import FunctionItem

from menuclasses.not_implemented_item import NotImplementedItem
from menufunctions.sale import sale_return
from .sale_menu import sale_menu
from .store_menu import store_menu
from .employee_menu import employee_menu
from .report_menu import report_menu

from sql import LegoDB


def employee_main_menu(database: LegoDB):
    # TODO: perhaps add a way for employees to clock in/out
    menu = ConsoleMenu('Welcome, Employee',
                       exit_option_text='Log Out')

    for item in (FunctionItem('Start a Sale', sale_menu, [database]),
                 FunctionItem('Start a Return', sale_return, [database]),
                 NotImplementedItem('NYI: Inventory Management'),  # order/delivery
                 FunctionItem('Employee Management', employee_menu, [database]),
                 FunctionItem('NYI: Store Management', store_menu, [database]),
                 FunctionItem('Reports', report_menu, [database])):
        menu.append_item(item)
    menu.show()

    # if employee is a manager, add more menu options
