from consolemenu import ConsoleMenu
from consolemenu.items import FunctionItem

from menuclasses.not_implemented_item import NotImplementedItem


def inventory_menu(context: dict):
    menu = ConsoleMenu('Inventory Management', exit_option_text='Return to Main Menu')
    for item in (NotImplementedItem('Create Order'),
                 NotImplementedItem('Cancel Open Order'),
                 NotImplementedItem('View Order History')):
        menu.append_item(item)
    menu.show()