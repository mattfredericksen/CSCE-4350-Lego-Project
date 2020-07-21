"""This menu is shown when customers select "Browse Bricks & Sets"."""

from consolemenu import ConsoleMenu
from consolemenu.items import FunctionItem

from menufunctions.browse import browse
from menufunctions.search import search


def browse_menu(context: dict):
    menu = ConsoleMenu('Browse & Search LEGO Products',
                       exit_option_text='Return to Main Menu')

    for item in (FunctionItem('Browse Bricks', browse, (context, 'Brick')),
                 FunctionItem('Browse Sets', browse, (context, 'Set')),
                 FunctionItem('Search All', search, (context,))):
        menu.append_item(item)
    menu.show()
