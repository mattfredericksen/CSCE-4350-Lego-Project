"""For more information, visit https://bit.ly/2Cp05L7"""

from consolemenu import ConsoleMenu
from consolemenu.items import FunctionItem

from menufunctions.sale import *

from sql import LegoDB


def sale_menu(database: LegoDB):
    """Display main sale menu"""

    # sale context is maintained across menu functions
    sale_items = {}

    menu = ConsoleMenu('Sale In Progress', show_exit_option=False)
    for item in (FunctionItem('Add items to sale', add,
                              [database, sale_items]),
                 FunctionItem('Remove items from sale', remove, [sale_items]),
                 FunctionItem('View current sale items', view, [sale_items]),
                 FunctionItem('Complete sale', complete,
                              [database, sale_items], should_exit=True),
                 FunctionItem('Cancel sale', confirm_exit,
                              [sale_items], should_exit=True)):
        menu.append_item(item)

    while not menu.returned_value:
        # Only complete() and confirm_exit() will get here.
        # If they return True, the sale has ended.
        menu.show()
