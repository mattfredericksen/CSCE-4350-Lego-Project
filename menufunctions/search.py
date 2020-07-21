"""This function might be gerneralizable for reuse."""

from fuzzywuzzy import process
from menus.selection_menu import SelectionMenuFromTuples

from .details import brick_details, set_details

from test_data.static import bricks, sets


def search():
    query = input('Search Query: ')
    choices = {key: f'{key} {value["name"]} {value["description"]}'
               for key, value in sets.items()}
    # TODO: guarantee that brick ids and set ids do not overlap
    choices.update({key: f'{key} {value["description"]}'
                    for key, value in bricks.items()})
    matches = process.extractBests(query, choices, score_cutoff=50, limit=25)

    matches = tuple((i := match[2],
                     (sets[i]['name'] if i in sets else bricks[i]['description']))
                    for match in matches)

    description = 'Select an item to view more details or ' \
                  'to add it to your cart'
    browser = SelectionMenuFromTuples(matches, title="Search Results",
                                      prologue_text=description,
                                      epilogue_text=description,
                                      exit_option_text='Return')
    while True:
        browser.show()
        if browser.selected_item.text == 'Return':
            break
        else:
            if (i := browser.selected_item.index) in sets:
                set_details(i)
            else:
                brick_details(i)
