from consolemenu import ConsoleMenu
from consolemenu.items import FunctionItem
from datetime import datetime

from menufunctions.sale import print_sale

from sql import LegoDB


def print_order(database: LegoDB, order_id: int, order_time,
                price, status, delivery_time):
    total_quantity = 0
    print('ORDER DETAILS:\n\n'
          'ITEMS\n---------------')
    for name, quantity in database.get_customer_orders(order_id):
        total_quantity += quantity
        print(f'(Qty: {quantity}) {name}')
    print(f'\nTotal quantity: {total_quantity}\n'
          f'Total price: ${price:,.2f}\n\n'
          f'Date ordered: {order_time:%c}\n'
          f'Order Status: {status}')
    if status == 'Delivered':
        print(f'Delivered on: {delivery_time:%c}')
    elif status in ('Processing', 'Shipping'):
        if delivery_time:
            print(f'Expected delivery: {delivery_time:%c}')
        else:
            print('Expected delivery: Unknown')
    input('\nPress [enter] to return.')


def order_menu(database: LegoDB):
    # TODO: Add a menu option for cancelling open orders
    menu = ConsoleMenu('Order History',
                       exit_option_text='Return to Main Menu')

    for order_id, order_time, price, status, delivery_time  \
            in database.get_customer_orders():
        text = f'({order_time:%c}) Total: ${price:,.2f}, Status: {status}'
        menu.append_item(FunctionItem(text, print_order,
                                      [database, order_id, order_time,
                                       price, status, delivery_time]))
    menu.show()
