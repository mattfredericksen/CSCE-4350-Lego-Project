from consolemenu import ConsoleMenu
from consolemenu.items import FunctionItem

from menufunctions.browse import browse_bricks, browse_sets
from menufunctions.search import search

browse_menu = ConsoleMenu('Browse & Search LEGO Products',
                          exit_option_text='Return to Main Menu')

for item in (FunctionItem('Browse Bricks', browse_bricks),
             FunctionItem('Browse Sets', browse_sets),
             FunctionItem('Search All', search)):
    browse_menu.append_item(item)
