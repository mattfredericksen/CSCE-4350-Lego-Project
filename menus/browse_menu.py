from consolemenu import ConsoleMenu
from consolemenu.items import FunctionItem, SubmenuItem

from .not_implemented_item import NotImplementedItem

# TODO: Think about how we want to implement orders.
#       Perhaps when an item is selected for more details,
#       we can show an 'add to cart' option with qty input.
#       Do we want a 'shopping cart' menu instead of 'Place an Order'?

browse_menu = ConsoleMenu('Browse LEGO Products',
                          exit_option_text='Return to Main Menu')

for item in (NotImplementedItem('Browse Bricks'),
             NotImplementedItem('Browse Sets'),
             NotImplementedItem('Browse All'),
             NotImplementedItem('Search All')):
    browse_menu.append_item(item)
