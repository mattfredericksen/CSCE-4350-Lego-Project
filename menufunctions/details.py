"""This functions might be gerneralizable for reuse."""

from consolemenu.screen import Screen

from typing import Literal

from test_data.static import bricks, sets


def details(context: dict, item_id: int, mode: Literal['Set', 'Brick']):
    while True:
        print('ITEM DETAILS\n')

        # display the attributes corresponding to the item type
        print(f'Item ID: {item_id}')
        if mode is 'Set':
            item = sets[item_id]
            print(f'Name: {item["name"]}',
                  f'Description: {item["description"]}',
                  f'Price: ${item["price"]}',
                  f'Piece count: {sum(qty for qty in item["set_items"].values())}',
                  f'Inventory: {item["inventory"]}', sep='\n')
        else:
            item = bricks[item_id]
            print(f'Description: {item["description"]}',
                  f'Price: ${item["price"]}',
                  f'Inventory: {item["inventory"]}', sep='\n')

        print('\nEnter a quantity to add this item to your cart.\n'
              'Enter nothing to return to browsing.\n')

        if not (quantity := input('>> ')):
            # if the user enters nothing, return to browsing menu
            break
        try:
            quantity = int(quantity)
        except ValueError:
            # if the user enters NaN, just reprompt
            Screen.clear()
        else:
            if quantity > 0:
                # TODO: run SQL to add stuff to cart
                cart_items = context['cart'][mode.lower() + 's']
                cart_items[item_id] = cart_items.get(item_id, 0) + quantity
                Screen.clear()
                input('Added item(s) to cart (not really).\n\n'
                      'Press [enter] to return to browsing.')
                break
            elif quantity == 0:
                break
