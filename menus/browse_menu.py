from consolemenu import ConsoleMenu
from consolemenu.items import FunctionItem, SubmenuItem

from .not_implemented_item import NotImplementedItem

browse_menu = ConsoleMenu('Browse LEGO Products',
                          exit_option_text='Return to Main Menu')

for item in (NotImplementedItem('Browse Bricks'),
             NotImplementedItem('Browse Sets'),
             NotImplementedItem('Browse All'),
             NotImplementedItem('Search All')):
    browse_menu.append_item(item)
