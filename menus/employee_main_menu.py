from consolemenu import ConsoleMenu
from consolemenu.items import FunctionItem, SubmenuItem

from .not_implemented_item import NotImplementedItem

# \/\/\/\/ MAIN MENU \/\/\/\/

employee_main_menu = ConsoleMenu('Welcome, working-class scum', exit_option_text='Log Out')

for item in (NotImplementedItem('Sales'),
             NotImplementedItem('Order Management'),
             NotImplementedItem('Delivery Management')):
    employee_main_menu.append_item(item)
