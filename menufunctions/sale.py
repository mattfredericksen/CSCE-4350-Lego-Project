"""For more information, visit https://bit.ly/2Cp05L7"""

from consolemenu.screen import Screen
from menuclasses.selection_menu import SelectionMenuFromTuples

from typing import Literal

from test_data.static import sets, bricks


def add(context: dict, sale_items: dict, mode: Literal['Set', 'Brick']) -> None:
    """Add an item to the current sale"""

    # exit loop when user enters nothing
    while product_id := input(f'{mode} ID [enter nothing to return]: '):
        try:
            product_id = int(product_id)
        except ValueError:
            Screen.clear()
            print(f'"{product_id}" is not a valid {mode} ID.\n')
            continue

        # check validity of product_id
        if product_id not in (sets if mode is 'Set' else bricks):
            Screen.clear()
            print(f'"{product_id}" is not a valid {mode} ID.\n')
            continue

        # get quantity of product to add to sale
        quantity = input(f'Quantity: ')
        try:
            if (quantity := int(quantity)) < 0:
                raise ValueError
        except ValueError:
            Screen.clear()
            print(f'"{quantity}" is not a valid quantity.\n')
            continue

        if quantity == 0:
            continue

        # add to or create entry depending on if it already exists
        sale_items[product_id] = sale_items.get(product_id, 0) + quantity
        Screen.clear()
        print(f'Added {quantity} items to the sale.\n')


def remove(context: dict, sale_items: dict) -> None:
    """Remove an item from the current sale"""

    sale_sets, sale_bricks = sale_items['sets'], sale_items['bricks']

    # combine sets and bricks into a single list for displaying
    items = [(i, f'(Qty: {q}) {sets[i]["name"]}')
             for i, q in sale_sets.items()] +  \
            [(i, f'(Qty: {q}) {bricks[i]["description"]}')
             for i, q in sale_bricks.items()]

    menu = SelectionMenuFromTuples(items, 'Remove Items from Sale',
                                   exit_option_text='Return to Sale')
    while True:
        menu.show()
        if (menu_item := menu.selected_item) is menu.exit_item:
            # return to the "Sale" menu
            break

        print('REMOVING ITEM\n')
        print(menu_item.text, '\n')

        # retrieve and validate quantity to remove
        quantity = input('How many should be removed? [enter nothing to cancel]: ')
        try:
            quantity = int(quantity)
        except ValueError:
            continue

        if quantity < 1:
            continue

        # get set or brick id
        item_id = menu_item.index
        # discover whether id is a set or brick
        items = sale_sets if item_id in sale_sets else sale_bricks

        if quantity < items[item_id]:
            # if some items will remain after removing:
            # get length of number for reforming string
            qty_len = len(str(items[item_id]))
            # adjust cart quantity
            items[item_id] -= quantity
            # adjust "Remove" menu text for this item
            menu_item.text = f'(Qty: {items[item_id]})' + menu_item.text[(7 + qty_len):]
        else:
            # if no items will remain after removing:
            del items[item_id]
            menu.remove_item(menu_item)


def print_sale(context: dict, sale_items: dict,
               title: str, prompt: str) -> str:
    """Print current sale items in a receipt-like format"""
    total_quantity = 0
    total_price = 0.0
    print(title, '\n\n'
          'Quantity | Unit Price | Item\n'
          '-------- | ---------- | ---------------')
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
        print(f'{quantity:8} | {price:>10} | {item["description"]}')
    print('\nTotals\n'
          '------\n'
          f'| Quantity: {total_quantity}\n'
          f'| Price: ${total_price:,.2f}\n')
    return input(prompt).lower()


def view(context: dict, sale_items: dict) -> None:
    """Print the sale. No modification."""
    print_sale(context, sale_items, 'SALE IN PROGRESS',
               'Press [enter] to return to the sale.')


def complete(context: dict, sale_items: dict) -> bool:
    # choose payment option
    # process payment
    # record sale in database
    # return to main menu
    pass


def confirm_exit(context: dict, sale_items: dict) -> bool:
    """Confirm exiting of sale when items have been entered.
    Returns True if exit should occur, False otherwise
    """

    # no need to confirm when no items have been entered
    if not (sale_items['sets'] or sale_items['bricks']):
        return True

    while True:
        answer = print_sale(context, sale_items, 'CONFIRM SALE CANCELLATION',
                            'Are you sure you want to cancel this sale? [y/n]: ')
        if answer in ('y', 'ye', 'yes'):
            return True
        elif answer in ('n', 'no'):
            return False
        else:
            Screen.clear()
