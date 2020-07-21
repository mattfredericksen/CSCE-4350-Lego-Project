"""These functions might be gerneralizable for reuse."""

from menus.selection_menu import SelectionMenuFromTuples
from .details import brick_details, set_details

from test_data.static import bricks, sets


def browse_bricks():
    description = 'Select an item to view more details or '  \
                  'to add it to your cart'
    bricks_partial = [(key, value['description']) for key, value in bricks.items()]
    browser = SelectionMenuFromTuples(bricks_partial, title='Browse Bricks',
                                      prologue_text=description,
                                      epilogue_text=description,
                                      exit_option_text='Return')
    while True:
        browser.show()
        if browser.selected_item is browser.exit_item:
            break
        else:
            brick_details(browser.selected_item.index)


def browse_sets():
    description = 'Select a set to view more details or '  \
                  'to add it to your cart'
    sets_partial = [(key, value['name']) for key, value in sets.items()]
    browser = SelectionMenuFromTuples(sets_partial, title='Browse Sets',
                                      prologue_text=description,
                                      epilogue_text=description,
                                      exit_option_text='Return')
    while True:
        browser.show()
        if browser.selected_item is browser.exit_item:
            break
        else:
            set_details(browser.selected_item.index)
