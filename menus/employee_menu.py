from consolemenu import ConsoleMenu
from consolemenu.items import FunctionItem

from menufunctions.employee import *


def employee_menu(context: dict):
    menu = ConsoleMenu('Employee Management', exit_option_text='Return to Main Menu')
    for item in (FunctionItem('View employees', view, [context]),
                 FunctionItem('Create employee', create, [context]),
                 FunctionItem('Remove employee', remove, [context])):
        menu.append_item(item)
    menu.show()
