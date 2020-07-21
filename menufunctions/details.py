"""These functions might be gerneralizable for reuse."""

from consolemenu.screen import Screen

from test_data.static import bricks, sets


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
