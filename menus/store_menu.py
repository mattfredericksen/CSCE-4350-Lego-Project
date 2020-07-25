from consolemenu import ConsoleMenu
from consolemenu.items import FunctionItem

from menufunctions.store import *
from menuclasses.not_implemented_item import NotImplementedItem

from sql import LegoDB


def store_menu(database: LegoDB):
    menu = ConsoleMenu('Store Management', exit_option_text='Return to Main Menu')
    for item in (FunctionItem('View Stores', view, [database]),
                 FunctionItem('Create Store', create, [database]),
                 NotImplementedItem('Remove Store')):
        menu.append_item(item)
    menu.show()
