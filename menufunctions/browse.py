"""This functions might be gerneralizable for reuse."""

from menus.selection_menu import SelectionMenuFromTuples
from .details import details

from typing import Literal

from test_data.static import bricks, sets


def browse(mode: Literal['Set', 'Brick']):
    description = 'Select an item to view more details or '  \
                  'to add it to your cart'
    if mode is 'Set':
        partial = [(key, value['name']) for key, value in sets.items()]
    else:
        partial = [(key, value['description']) for key, value in bricks.items()]

    browser = SelectionMenuFromTuples(partial, title=f'Browse {mode}s',
                                      prologue_text=description,
                                      epilogue_text=description,
                                      exit_option_text='Return')

    while True:
        browser.show()
        if browser.selected_item is browser.exit_item:
            break
        details(browser.selected_item.index, mode)
