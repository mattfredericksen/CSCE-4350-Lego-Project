from consolemenu import ConsoleMenu
from consolemenu.items import FunctionItem, SubmenuItem

from .customer_account_menu import account_menu

# \/\/\/\/ MAIN MENU \/\/\/\/

main_menu = ConsoleMenu('Welcome to The Lego Store', exit_option_text='Log Out')

browse_item = FunctionItem('Browse Bricks & Sets', input, ['not yet implemented'])
order_item = FunctionItem('Place an Order', input, ['not yet implemented'])

account_item = SubmenuItem('Account Information', account_menu, menu=main_menu)

main_menu.append_item(browse_item)
main_menu.append_item(order_item)
main_menu.append_item(account_item)