"""This is the first menu customers see upon logging in."""

from consolemenu import ConsoleMenu
from consolemenu.items import FunctionItem, SubmenuItem

from .customer_account_menu import account_menu
from .browse_menu import browse_menu
from .not_implemented_item import NotImplementedItem


main_menu = ConsoleMenu('Welcome to The Lego Store',
                        exit_option_text='Log Out')

for item in (SubmenuItem('Browse Bricks & Sets', browse_menu),
             NotImplementedItem('Checkout'),
             NotImplementedItem('Order History'),
             SubmenuItem('Account Information', account_menu)):
    main_menu.append_item(item)
