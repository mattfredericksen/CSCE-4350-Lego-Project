"""This is the first menu customers see upon logging in."""

from consolemenu import ConsoleMenu
from consolemenu.items import FunctionItem

from .customer_account_menu import account_menu
from .browse_menu import browse_menu
from menufunctions.checkout import checkout
from menuclasses.not_implemented_item import NotImplementedItem


def main_menu(context: dict):
    context.setdefault('cart', {'sets': {}, 'bricks': {}})

    menu = ConsoleMenu('Welcome to The Lego Store',
                       exit_option_text='Log Out')

    for item in (FunctionItem('Browse Bricks & Sets', browse_menu, [context]),
                 FunctionItem('Checkout', checkout, [context]),
                 NotImplementedItem('Order History'),
                 FunctionItem('Account Information', account_menu, [context])):
        menu.append_item(item)
    menu.show()
