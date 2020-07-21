"""This menu is shown when customers select "Browse Bricks & Sets"."""

from consolemenu import ConsoleMenu
from consolemenu.items import FunctionItem

from menufunctions.browse import browse
from menufunctions.search import search

browse_menu = ConsoleMenu('Browse & Search LEGO Products',
                          exit_option_text='Return to Main Menu')

for item in (FunctionItem('Browse Bricks', browse, ('Brick',)),
             FunctionItem('Browse Sets', browse, ('Set',)),
             FunctionItem('Search All', search)):
    browse_menu.append_item(item)
