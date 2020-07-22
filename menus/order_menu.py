from consolemenu import ConsoleMenu
from consolemenu.items import FunctionItem
from datetime import datetime

from menufunctions.sale import print_sale

from test_data.static import orders


def order_menu(context: dict):
    # TODO: Add a menu option for cancelling open orders
    menu = ConsoleMenu('Order History',
                       exit_option_text='Return to Main Menu')

    for oid, order in orders.items():
        date = datetime.fromisoformat(order['date']).strftime('%x')
        text = f'({date}) Total: ${order["price"]:,.2f}, Status: {order["status"]}'
        menu.append_item(FunctionItem(text, print_sale,
                                      [context, order['items'],
                                       f'ORDER FROM {date} ({order["status"]})',
                                       'Press [enter] to return.']))
    menu.show()
