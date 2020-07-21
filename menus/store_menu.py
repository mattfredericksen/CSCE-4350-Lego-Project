from consolemenu import ConsoleMenu
from consolemenu.items import FunctionItem

from menufunctions.store import *
from menuclasses.not_implemented_item import NotImplementedItem


def store_menu(context: dict):
    menu = ConsoleMenu('Store Management', exit_option_text='Return to Main Menu')
    for item in (FunctionItem('View Stores', view, (context,)),
                 FunctionItem('Create Store', create, (context,)),
                 NotImplementedItem('Remove Store')):
        menu.append_item(item)
    menu.show()
