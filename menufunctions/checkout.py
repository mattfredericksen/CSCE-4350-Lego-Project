from consolemenu import ConsoleMenu
from consolemenu.items import FunctionItem

from .details import details
from menus.payment_menu import payment_menu

from sql import LegoDB


def print_cart(database: LegoDB) -> bool:
    """Print current sale items in a receipt-like format"""
    total_quantity = 0
    total_price = 0.0
    print('CART TOTALS\n\n'
          'Quantity | Unit Price | Item\n'
          '-------- | ---------- | ---------------')
    for _, name, quantity, price in database.get_cart():
        total_quantity += quantity
        total_price += quantity * price
        price = f'${price:,.2f}'
        print(f'{quantity:8} | {price:>10} | {name}')
    print('\nTotals\n'
          '------\n'
          f'| Quantity: {total_quantity}\n'
          f'| Price: ${total_price:,.2f}\n')

    choice = input('Continue to Payment Method? [y/n]: ').lower()
    if choice in ('y', 'ye', 'yes'):
        return select_payment(database)
    else:
        return False


def select_payment(database: LegoDB) -> bool:
    if payment := payment_menu(database):
        database.checkout(payment)
        input('Order Completed. Press [enter] to return.')
        return True
    else:
        return False


def checkout(database: LegoDB):
    instructions = 'Select an item to modify its quantity.'
    menu = ConsoleMenu('Checkout', exit_option_text='Return to Main Menu',
                       prologue_text=instructions,
                       epilogue_text=instructions)
    for idx, description, qty, _ in database.get_cart():
        menu.append_item(FunctionItem(f'(Qty: {qty}) {description}',
                                      details, [database, idx],
                                      should_exit=True))

    continue_item = FunctionItem('Continue to View Totals', print_cart,
                                 [database], should_exit=True)
    menu.append_item(continue_item)

    while True:
        if len(list(filter(lambda i: isinstance(i, FunctionItem), menu.items))) < 2:
            input('Cart is empty. Press [enter] to return.')
            return
        menu.show()
        if (menu_item := menu.selected_item) is menu.exit_item:
            return
        elif menu_item is continue_item:
            if menu.returned_value:
                return
            else:
                continue
        elif (qty := menu.returned_value) is None:
            continue
        elif qty == 0:
            menu.remove_item(menu_item)
        else:
            menu_item.text = f'(Qty: {qty}{menu_item.text[menu_item.text.find(")"):]}'
