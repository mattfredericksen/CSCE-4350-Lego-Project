"""This is the menu that employees see upon logging in."""

from consolemenu import ConsoleMenu
from consolemenu.items import FunctionItem, SubmenuItem

from .not_implemented_item import NotImplementedItem
from menufunctions.sale import sale


employee_main_menu = ConsoleMenu('Welcome, working-class scum',
                                 exit_option_text='Log Out')

for item in (FunctionItem('Start a Sale', sale),
             NotImplementedItem('Start a Return'),
             NotImplementedItem('Order Management'),
             NotImplementedItem('Delivery Management')):
    employee_main_menu.append_item(item)
