from consolemenu import ConsoleMenu
from consolemenu.items import FunctionItem
from .not_implemented_item import NotImplementedItem


# \/\/\/ CUSTOMER ACCOUNT MENU \/\/\/

account_menu = ConsoleMenu('Account Information', exit_option_text='Return to Main Menu')
for item in (NotImplementedItem('Change Username'),
             NotImplementedItem('Change Password'),
             NotImplementedItem('Change Email'),
             NotImplementedItem('Change Payment Options'),
             NotImplementedItem('Change Shipping Address'),
             NotImplementedItem('Change Store Preference')):
    account_menu.append_item(item)
