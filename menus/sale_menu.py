"""For more information, visit https://bit.ly/2Cp05L7"""

from consolemenu import ConsoleMenu
from consolemenu.items import FunctionItem

from menufunctions.sale import *


def sale_menu(context: dict):
    """Display main sale menu"""

    # sale context is maintained across menu functions
    sale_items = {'sets': {}, 'bricks': {}}

    menu = ConsoleMenu('Sale In Progress', show_exit_option=False)
    for item in (FunctionItem('Add sets to sale', add,
                              (context, sale_items['sets'], 'Set')),
                 FunctionItem('Add bricks to sale', add,
                              (context, sale_items['bricks'], 'Brick')),
                 FunctionItem('Remove items from sale', remove,
                              (context, sale_items)),
                 FunctionItem('View current sale items', view,
                              (context, sale_items)),
                 FunctionItem('Complete sale', complete,
                              (context, sale_items), should_exit=True),
                 FunctionItem('Cancel sale', confirm_exit,
                              (context, sale_items), should_exit=True)):
        menu.append_item(item)

    while not menu.returned_value:
        # Only complete() and confirm_exit() will get here.
        # If they return True, the sale has ended.
        menu.show()
