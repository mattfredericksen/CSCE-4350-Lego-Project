"""This functions might be gerneralizable for reuse."""

from menuclasses.selection_menu import SelectionMenuFromTuples
from .details import details

from .sql import get_sets, get_bricks


def browse(context: dict, set_mode: bool):
    """Display a menu with all available Sets or Bricks.
    When the user selects an item, its details are displayed
    with an option to add that item to their cart.
    """

    instructions = 'Select an item to view more details or '  \
                   'to add it to your cart.'
    items = get_sets(description=False) if set_mode else get_bricks()

    browser = SelectionMenuFromTuples(items, title=f'Browse {"Sets" if set_mode else "Bricks"}',
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
        details(context, browser.selected_item.index)
