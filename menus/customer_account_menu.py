"""This menu is shown when customers select "Account Information"."""

from consolemenu import ConsoleMenu
from consolemenu.items import FunctionItem
from menuclasses.not_implemented_item import NotImplementedItem


### MENU FUNCTIONS IN HERE ###




###############################

def account_menu(context: dict):
    menu = ConsoleMenu('Account Information', exit_option_text='Return to Main Menu')
    for item in (NotImplementedItem('Change Username'),
                 NotImplementedItem('Change Password'),
                 NotImplementedItem('Change Email'),
                 NotImplementedItem('Change Payment Options'),
                 NotImplementedItem('Change Shipping Address'),
                 NotImplementedItem('Change Store Preference')):
        menu.append_item(item)
    menu.show()
