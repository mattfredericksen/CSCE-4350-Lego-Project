"""For more information, visit https://bit.ly/2Cp05L7"""

from consolemenu.screen import Screen
from menuclasses.selection_menu import SelectionMenuFromTuples

from sql import LegoDB


def add(database: LegoDB, sale_items: dict) -> None:
    """Add an item to the current sale"""

    # exit loop when user enters nothing
    while item_id := input(f'Item ID [enter nothing to return]: '):
        try:
            item_id = int(item_id)
        except ValueError:
            Screen.clear()
            print(f'"{item_id}" is not a valid Item ID.\n')
            continue

        # check validity of product_id
        # assume original schema designation of set/bricks IDs applies
        try:
            item = database.get_sets(item_id)  \
                if item_id < 10000 else database.get_bricks(item_id)
        except ValueError:
            Screen.clear()
            print(f'"{item_id}" is not a valid Item ID.\n')
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
        if item_id in sale_items:
            sale_items[item_id]['quantity'] += quantity
        else:
            sale_items[item_id] = {
                'name': item[1],
                'price': database.get_set_price(item_id)
                             if item_id < 10000 else item[2],
                'quantity': quantity
            }
        Screen.clear()
        print(f'Added {quantity} "{item[1]}" to the sale.\n')


def remove(sale_items: dict) -> None:
    """Remove an item from the current sale"""

    # combine sets and bricks into a single list for displaying
    items = [(idx, f'(Qty: {item["quantity"]}) {item["name"]}')
             for idx, item in sale_items.items()]

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
            if (quantity := int(quantity)) < 1:
                continue
        except ValueError:
            continue

        # get set or brick
        item = sale_items[menu_item.index]

        if quantity < item['quantity']:
            # adjust cart quantity
            item['quantity'] -= quantity
            # adjust "Remove" menu text for this item
            menu_item.text = f'(Qty: {item["quantity"]}' \
                             f'{menu_item.text[menu_item.text.find(")"):]}'
        else:
            # if no items will remain after removing:
            del sale_items[menu_item.index]
            menu.remove_item(menu_item)


def print_sale(sale_items: dict, title: str, prompt: str) -> str:
    """Print current sale items in a receipt-like format"""
    total_quantity = 0
    total_price = 0.0
    print(title, '\n\n'
          'Quantity | Unit Price | Item\n'
          '-------- | ---------- | ---------------')
    for item_id, item in sale_items.items():
        total_quantity += item['quantity']
        total_price += item['price'] * item['quantity']
        price = f'${item["price"]:,.2f}'
        print(f'{item["quantity"]:8} | {price:>10} | {item["name"]}')
    print('\nTotals\n'
          '------\n'
          f'| Quantity: {total_quantity}\n'
          f'| Price: ${total_price:,.2f}\n')
    return input(prompt).lower()


def view(sale_items: dict) -> None:
    """Print the sale. No modification."""
    print_sale(sale_items, 'SALE IN PROGRESS', 'Press [enter] to return to the sale.')


def complete(database: LegoDB, sale_items: dict) -> bool:
    if print_sale(sale_items, 'SALE CONFIRMATION',
                  'Continue to payment? [y/n]: ')  \
            not in ('y', 'ye', 'yes'):
        return False
    Screen.clear()

    print('CASH OR CREDIT\n\n'
          'If customer is paying via credit card, type it in.\n'
          'Otherwise, press [enter] after accepting the cash.\n')
    card = input('>> ')
    try:
        database.create_sale(sale_items, card)
    except Exception as e:
        print(f'\n{e}')
        input('Failed to process sale. Press [enter] to return.')
    else:
        input('Transaction completed. Press [enter] to continue.')
        return True


def confirm_exit(sale_items: dict) -> bool:
    """Confirm exiting of sale when items have been entered.
    Returns True if exit should occur, False otherwise
    """

    # no need to confirm when no items have been entered
    if not sale_items:
        return True

    while True:
        answer = print_sale(sale_items, 'CONFIRM SALE CANCELLATION',
                            'Are you sure you want to cancel this sale? [y/n]: ')
        if answer in ('y', 'ye', 'yes'):
            return True
        elif answer in ('n', 'no'):
            return False
        else:
            Screen.clear()


def sale_return(database: LegoDB):
    print('SALE RETURN\n')
    try:
        sale_id = int(input('Enter Sale ID# from customer\'s receipt: '))
    except ValueError:
        input('Invalid Sale ID#. Press [enter] to return.')
        return

    if database.is_sale_returned(sale_id):
        input('\nSale has already been returned. Press [enter] to return.')
        return
    elif not (sale_items := database.get_sale(sale_id)):
        input('Sale does not exist. Press [enter] to return.')
        return

    Screen.clear()
    print('SALE RETURN ITEMS\n')
    for item_id, qty, *_ in sale_items:
        name = database.get_sets(item_id)[1]  \
            if item_id < 10000 else database.get_bricks(item_id)[1]
        print(f'(Qty: {qty}) {name}')
    print(f'\nTotal: ${sale_items[0][2]:,.2f}\n')

    if not (reason := input('Reason for return [enter nothing to cancel]: ')):
        return

    if card := sale_items[0][3]:
        input(f'\nCustomer\'s money will be refunded to card ending in {card}.\n'
              'Press [enter] to complete return.')
    else:
        input(f'\nCustomer payed with cash. Refund them ${sale_items[0][2]:,.2f}'
              'Press [enter] to complete return.')

    try:
        database.create_return(sale_id, reason)
    except Exception as e:
        print(f'\n{e}')
        input('Failed to process return. Press [enter] to continue.')
