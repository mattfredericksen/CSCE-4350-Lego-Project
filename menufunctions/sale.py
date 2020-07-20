from consolemenu import ConsoleMenu
from consolemenu.items import FunctionItem
from consolemenu.screen import Screen
from typing import Literal

from menus.not_implemented_item import NotImplementedItem

from test_data.static import sets, bricks


def add(sale_items, mode: Literal['Set', 'Brick']):
    while True:
        product_id = input(f'{mode} ID [enter nothing to return]: ')
        try:
            product_id = int(product_id)
        except ValueError:
            if product_id == '':
                return
            continue

        if product_id not in (sets if mode is 'Set' else bricks):
            Screen.clear()
            print(f'"{product_id}" is not a valid {mode} ID.\n')
            continue

        # Forcing inventory accuracy could have some
        # negative consequences in the real world.
        #
        # if (inventory := product['inventory']) == 0:
        #     Screen.clear()
        #     print(f'"{descriptor}" is out of stock.\n')
        #     continue

        quantity = input(f'Quantity: ')
        try:
            if (quantity := int(quantity)) < 1:
                raise ValueError
        except ValueError:
            Screen.clear()
            print(f'"{quantity}" is not a valid quantity.\n')
            continue

        # if not 1 <= quantity <= inventory:
        #     Screen.clear()
        #     print(f'"{quantity}" is out of inventory range [1-{inventory}].\n')
        #     continue

        # add to or create entry depending on if it already exists
        sale_items[product_id] = sale_items.get(product_id, 0) + quantity


def remove(sale_items):
    pass


def view(sale_items):
    pass


def complete(sale_items):
    pass


def sale():
    sale_items = {'sets': {}, 'bricks': {}}

    menu = ConsoleMenu('Sale In Progress', exit_option_text='Cancel sale')
    for item in (FunctionItem('Add set(s) to sale', add,
                              [sale_items['sets'], 'Set']),
                 FunctionItem('Add brick(s) to sale', add,
                              [sale_items['bricks'], 'Brick']),
                 NotImplementedItem('Remove item from sale'),
                 NotImplementedItem('View current sale items'),
                 NotImplementedItem('Complete sale')):
        menu.append_item(item)
    menu.show()
