"""This functions might be gerneralizable for reuse."""

from menus.selection_menu import SelectionMenuFromTuples
from .details import details

from typing import Literal

from test_data.static import bricks, sets


def browse(mode: Literal['Set', 'Brick']):
    """Display a menu with all available Sets or Bricks.
    When the user selects an item, its details are displayed
    with an option to add that item to their cart.
    """

    instructions = 'Select an item to view more details or '  \
                   'to add it to your cart.'
    if mode is 'Set':
        items = [(key, value['name']) for key, value in sets.items()]
    else:
        items = [(key, value['description']) for key, value in bricks.items()]

    browser = SelectionMenuFromTuples(items, title=f'Browse {mode}s',
                                      prologue_text=instructions,
                                      epilogue_text=instructions,
                                      exit_option_text='Return')

    while True:
        browser.show()

        # Whenever we get here, the user has selected
        # an item from the menu. Unless they chose to exit,
        # we display the details of the item they selected
        # and then redisplay this browsing menu.

        if browser.selected_item is browser.exit_item:
            break
        details(browser.selected_item.index, mode)
