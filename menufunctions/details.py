from consolemenu.screen import Screen
from sql import LegoDB


def details(database: LegoDB, item_id: int):
    while True:
        user_id = 2  # TODO: fix this after login stuff is complete
        store_id = database.get_store_preference()
        print('ITEM DETAILS\n')

        # display the attributes corresponding to the item type
        print(f'Item ID: {item_id}')
        if item_id < 10000:
            item = database.get_sets(item_id)
            print(f'Name: {item[1]}',
                  f'Description: {item[2]}',
                  f'Price: ${database.get_set_price(item_id)}',
                  f'Piece count: {database.get_set_count(item_id)}',
                  f'Inventory: {database.get_set_inventory(item_id)}',
                  sep='\n')
        else:
            item = database.get_bricks(item_id)
            print(f'Description: {item[1]}',
                  f'Price: ${item[2]}',
                  f'Inventory: {database.get_brick_inventory(item_id)}',
                  sep='\n')

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
            database.modify_cart(item_id, quantity)
            if quantity > 0:
                Screen.clear()
                input('Item quantity has been set in your cart.\n\n'
                      'Press [enter] to return.')
                return quantity
            elif quantity == 0:
                Screen.clear()
                input('Item has been removed from your cart.\n\n'
                      'Press [enter] to return.')
                return quantity
        # if the user enters NaN or <0, just re-prompt
        Screen.clear()
