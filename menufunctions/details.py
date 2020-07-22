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

        print('\nSet the item quantity for your cart.\n'
              'Enter nothing to return.\n')

        if not (quantity := input('>> ')):
            # if the user enters nothing, return to previous menu
            return
        try:
            quantity = int(quantity)
        except ValueError:
            pass
        else:
            cart = context['cart'][mode.lower() + 's']
            if quantity > 0:
                # TODO: run SQL to modify stuff in cart
                cart[item_id] = quantity
                Screen.clear()
                input('Item quantity has been set in your cart.\n\n'
                      'Press [enter] to return.')
                return quantity
            elif quantity == 0:
                if item_id in cart:
                    # TODO: run SQL to remove stuff from cart
                    del cart[item_id]
                    Screen.clear()
                    input('Item has been removed from your cart.\n\n'
                          'Press [enter] to return.')
                return quantity
        # if the user enters NaN or <0, just re-prompt
        Screen.clear()
