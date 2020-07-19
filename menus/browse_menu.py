from consolemenu import ConsoleMenu
from consolemenu.items import FunctionItem
from consolemenu.screen import Screen

from fuzzywuzzy import process, utils

from .selection_menu import SelectionMenuFromTuples
from .not_implemented_item import NotImplementedItem
from test_data.static import bricks, sets

# TODO: refactor details & browse functions to work
#       for both bricks & sets


def brick_details(brick_id):
    while True:
        print('ITEM DETAILS\n')
        for key, value in bricks[brick_id].items():
            print(f'{key.title()}: {value}')
        print('\n')  # two newlines

        if (bricks[brick_id]['inventory']) > 0:
            print('Enter a quantity to add this item to your cart.')
        else:
            print('This item is out of stock at your preferred store.')

        print('Enter nothing to return to browsing.\n')

        choice = input('>> ')
        try:
            choice = int(choice)
        except ValueError:
            if choice == '':
                break
        else:
            if choice > 0:
                # TODO: run SQL to add stuff to cart
                Screen.clear()
                input('Added item(s) to cart (not really). Press [enter] to return to browsing.')
                break
            elif choice == 0:
                break
        Screen.clear()


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
        if browser.selected_item.text == 'Return':
            break
        else:
            brick_details(browser.selected_item.index)


def set_details(set_id):
    # TODO: consider using textwrap for better formatting
    #       of long set descriptions.
    while True:
        print('SET DETAILS\n')
        item = sets[set_id]
        print(f'Name: {item["name"]}',
              f'Description: {item["description"]}',
              f'Price: ${item["price"]}',
              f'Piece count: {sum(qty for qty in item["set_items"].values())}',
              f'Inventory: {item["inventory"]}', sep='\n')
        print('\n')  # two newlines

        if (sets[set_id]['inventory']) > 0:
            print('Enter a quantity to add this set to your cart.')
        else:
            print('This set is out of stock at your preferred store.')

        print('Enter nothing to return to browsing.\n')

        choice = input('>> ')
        try:
            choice = int(choice)
        except ValueError:
            if choice == '':
                break
        else:
            if choice > 0:
                # TODO: run SQL to add stuff to cart
                Screen.clear()
                input('Added set(s) to cart (not really). Press [enter] to return to browsing.')
                break
            elif choice == 0:
                break
        Screen.clear()


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
        if browser.selected_item.text == 'Return':
            break
        else:
            set_details(browser.selected_item.index)


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


browse_menu = ConsoleMenu('Browse & Search LEGO Products',
                          exit_option_text='Return to Main Menu')

for item in (FunctionItem('Browse Bricks', browse_bricks),
             FunctionItem('Browse Sets', browse_sets),
             FunctionItem('Search All', search)):
    browse_menu.append_item(item)
