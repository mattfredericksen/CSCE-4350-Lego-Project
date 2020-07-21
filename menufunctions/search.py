"""This function might be gerneralizable for reuse."""

from fuzzywuzzy import process
from menuclasses.selection_menu import SelectionMenuFromTuples

from .details import details

from test_data.static import bricks, sets


def search():
    query = input('Search Query: ')

    # Create the strings that will be fuzzy-searched. For sets,
    # this includes the id, name, and description.
    choices = {key: f'{key} {value["name"]} {value["description"]}'
               for key, value in sets.items()}

    # TODO: guarantee that brick ids and set ids do not overlap

    # Add bricks to the searchable strings
    choices.update({key: f'{key} {value["description"]}'
                    for key, value in bricks.items()})

    # drop anything below a 50% fuzzy-match
    # limit results to 25
    matches = process.extractBests(query, choices, score_cutoff=50, limit=25)

    # Display the matches to the user.
    # Unfortunately, we have to recompute whether
    # a match is a set or a brick.
    # Match tuples are (choice, score, key)
    matches = tuple((i := match[2],
                     (sets[i]['name'] if i in sets else bricks[i]['description']))
                    for match in matches)

    instructions = 'Select an item to view more details or ' \
                   'to add it to your cart'
    browser = SelectionMenuFromTuples(matches, title="Search Results",
                                      prologue_text=instructions,
                                      epilogue_text=instructions,
                                      exit_option_text='Return')
    while True:
        browser.show()

        # Whenever we get here, the user has selected
        # an item from the search results. Unless they chose
        # to exit, we display the details of the item they
        # selected and then redisplay this results menu.

        if browser.selected_item is browser.exit_item:
            # return to "Browse & Search"
            break
        else:
            # check whether the selection is a set or a brick
            # and display item details
            if (i := browser.selected_item.index) in sets:
                details(i, 'Set')
            else:
                details(i, 'Brick')
