"""This function might be gerneralizable for reuse."""

from fuzzywuzzy import process
from menuclasses.selection_menu import SelectionMenuFromTuples

from .details import details

from .sql import *


def search(context: dict):
    query = input('Search Query: ')

    # TODO: If I don't run out of time, swap this part
    #       out with a View that does the same thing
    # Create the strings that will be fuzzy-searched. For sets,
    # this includes the id, name, and description.
    choices = {sid: f'{sid} {name} {description}'
               for sid, name, description in get_sets()}

    # Add bricks to the searchable strings
    choices.update({bid: f'{bid} {description}'
                    for bid, description in get_bricks()})

    # drop anything below a 50% fuzzy-match
    # limit results to 25
    matches = process.extractBests(query, choices, score_cutoff=50, limit=25)

    # Display the matches to the user.
    # Match tuples are (choice, score, key)
    # i < 10000 relies on current schema
    matches = [(i := match[2],
               (get_sets(i)[1] if i < 10000 else get_bricks(i)[1]))
               for match in matches]

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
            if (i := browser.selected_item.index) < 10000:
                details(context, i, 'Set')
            else:
                details(context, i, 'Brick')
