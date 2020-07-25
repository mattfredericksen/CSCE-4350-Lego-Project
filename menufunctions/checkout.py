from consolemenu import ConsoleMenu
from consolemenu.items import FunctionItem

from .details import details
from .sale import print_sale
from menus.payment_menu import payment_menu

from menufunctions import sql


def print_cart(context: dict) -> bool:
    """Print current sale items in a receipt-like format"""
    total_quantity = 0
    total_price = 0.0
    print('CART TOTALS\n\n'
          'Quantity | Unit Price | Item\n'
          '-------- | ---------- | ---------------')
    for _, name, quantity, price in sql.get_cart(user_id=2):
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
        return select_payment(context)
    else:
        return False


def select_payment(context: dict) -> bool:
    if payment := payment_menu(context):
        sql.checkout(user_id=2, payment_id=payment)
        input('Order Completed. Press [enter] to return.')
        return True
    else:
        return False


def checkout(context: dict):
    instructions = 'Select an item to modify its quantity.'
    menu = ConsoleMenu('Checkout', exit_option_text='Return to Main Menu',
                       prologue_text=instructions,
                       epilogue_text=instructions)
    for idx, description, qty, _ in sql.get_cart(user_id=2):  # TODO: get real user_id
        menu.append_item(FunctionItem(f'(Qty: {qty}) {description}',
                                      details, [context, idx],
                                      should_exit=True))

    continue_item = FunctionItem('Continue to View Totals', print_cart,
                                 [context], should_exit=True)
    menu.append_item(continue_item)

    while True:
        if len(menu.items) < 3:
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
        elif qty is 0:
            menu.remove_item(menu_item)
        else:
            menu_item.text = f'(Qty: {qty}{menu_item.text[menu_item.text.find(")"):]}'
