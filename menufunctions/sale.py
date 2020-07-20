from consolemenu import ConsoleMenu
from consolemenu.items import FunctionItem
from consolemenu.screen import Screen
from menus.selection_menu import SelectionMenuFromTuples

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
    sale_sets, sale_bricks = sale_items['sets'], sale_items['bricks']
    items = [(i, f'(Qty: {q}) {sets[i]["name"]}')
             for i, q in sale_sets.items()] +  \
            [(i, f'(Qty: {q}) {bricks[i]["description"]}')
             for i, q in sale_bricks.items()]

    menu = SelectionMenuFromTuples(items, title="Remove Items from Sale",
                                   exit_option_text='Return to Sale')
    while True:
        menu.show()
        menu_item = menu.selected_item
        if menu_item is menu.exit_item:
            break
        item_id = menu_item.index

        print('REMOVING ITEM\n')
        print(menu_item.text, '\n')
        quantity = input('How many should be removed? [enter nothing to cancel]: ')
        try:
            quantity = int(quantity)
        except ValueError:
            if quantity == '':
                continue

        if quantity < 1:
            continue

        items = sale_sets if item_id in sale_sets else sale_bricks
        if quantity < items[item_id]:
            qty_len = len(str(items[item_id]))
            items[item_id] -= quantity
            menu_item.text = f'(Qty: {items[item_id]})' + menu_item.text[(7 + qty_len):]
        else:
            del items[item_id]
            menu.remove_item(menu_item)


def view(sale_items):
    total_quantity = 0
    total_price = 0.0
    print('SALE IN PROGRESS\n')
    print('Quantity | Unit Price | Items')
    print('-------- | ---------- | ---------------')
    for item_id, quantity in sale_items['sets'].items():
        item = sets[item_id]
        total_quantity += quantity
        total_price += item['price'] * quantity
        price = f'${item["price"]:.2f}'
        print(f'{quantity:8} | {price:>10} | {item["name"]}')
    for item_id, quantity in sale_items['bricks'].items():
        item = bricks[item_id]
        total_quantity += quantity
        total_price += item['price'] * quantity
        price = f'${item["price"]:.2f}'
        print(f'{quantity:8} | {price:>10} | {item["name"]}')
    print('\nTotals\n------')
    print(f'| Quantity: {total_quantity}')
    print(f'| Price: ${total_price:,.2f}')

    input('\nPress [enter] to return to sale.')


def complete(sale_items):
    pass


def sale():
    sale_items = {'sets': {}, 'bricks': {}}

    menu = ConsoleMenu('Sale In Progress', exit_option_text='Cancel sale')
    for item in (FunctionItem('Add sets to sale', add,
                              [sale_items['sets'], 'Set']),
                 FunctionItem('Add bricks to sale', add,
                              [sale_items['bricks'], 'Brick']),
                 FunctionItem('Remove items from sale', remove,
                              [sale_items]),
                 FunctionItem('View current sale items', view, [sale_items]),
                 NotImplementedItem('Complete sale')):
        menu.append_item(item)
    menu.show()
