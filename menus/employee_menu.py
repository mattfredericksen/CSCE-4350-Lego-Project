from consolemenu import ConsoleMenu
from consolemenu.items import FunctionItem
from menuclasses.not_implemented_item import NotImplementedItem


def employee_menu(context: dict):
    menu = ConsoleMenu('Employee Management', exit_option_text='Return to Main Menu')
    for item in (NotImplementedItem('View employees'),
                 NotImplementedItem('Create employee'),
                 NotImplementedItem('Remove employee')):
        menu.append_item(item)
    menu.show()
