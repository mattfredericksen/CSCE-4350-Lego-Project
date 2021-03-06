"""This menu is shown when customers select "Browse Bricks & Sets"."""

from consolemenu import ConsoleMenu
from consolemenu.items import FunctionItem

from menufunctions.browse import browse
from menufunctions.search import search

from sql import LegoDB


def browse_menu(database: LegoDB):
    menu = ConsoleMenu('Browse & Search LEGO Products',
                       exit_option_text='Return to Main Menu')

    for item in (FunctionItem('Browse Bricks', browse, [database, False]),
                 FunctionItem('Browse Sets', browse, [database, True]),
                 FunctionItem('Search All', search, [database])):
        menu.append_item(item)
    menu.show()
