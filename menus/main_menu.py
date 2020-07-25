"""This is the first menu customers see upon logging in."""

from consolemenu import ConsoleMenu
from consolemenu.items import FunctionItem

from .customer_account_menu import account_menu
from .browse_menu import browse_menu
from menufunctions.checkout import checkout
from .order_menu import order_menu

from sql import LegoDB


def main_menu(database: LegoDB):
    menu = ConsoleMenu('Welcome to The Lego Store',
                       exit_option_text='Log Out')

    for item in (FunctionItem('Browse Bricks & Sets', browse_menu, [database]),
                 FunctionItem('Checkout Cart', checkout, [database]),
                 FunctionItem('Order History', order_menu, [database]),
                 FunctionItem('Account Information', account_menu, [database])):
        menu.append_item(item)
    menu.show()
