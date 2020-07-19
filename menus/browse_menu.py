from consolemenu import ConsoleMenu
from consolemenu.items import FunctionItem
from consolemenu.screen import Screen

from .selection_menu import SelectionMenuFromTuples
from .not_implemented_item import NotImplementedItem
from test_data.bricks import generate_bricks


def brick_details(brick_id, bricks):
    while True:
        print('ITEM DETAILS\n')
        for key, value in bricks[brick_id].items():
            print(f'{key.title()}: {value}')
        print('\n')  # two newlines

        if (inventory := bricks[brick_id]['inventory']) > 0:
            print('Enter a quantity to add this item to your cart.')
        else:
            print('This item is out of stock at your preferred store.')

        print('Enter nothing to return to browsing.\n')

        try:
            choice = int(input('>> '))
        except ValueError:
            if choice == '':
                break
        else:
            if 1 <= choice <= inventory:
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
    bricks = generate_bricks()
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
            brick_details(browser.selected_item.index, bricks)


browse_menu = ConsoleMenu('Browse LEGO Products',
                          exit_option_text='Return to Main Menu')

for item in (FunctionItem('Browse Bricks', browse_bricks),
             NotImplementedItem('Browse Sets'),
             NotImplementedItem('Browse All'),
             NotImplementedItem('Search All')):
    browse_menu.append_item(item)
