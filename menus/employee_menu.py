from consolemenu import ConsoleMenu
from consolemenu.items import FunctionItem

from menufunctions.employee import *

from sql import LegoDB


def employee_menu(database: LegoDB):
    menu = ConsoleMenu('Employee Management', exit_option_text='Return to Main Menu')
    for item in (FunctionItem('View employees', view, [database]),
                 FunctionItem('Create employee', create, [database]),
                 FunctionItem('Remove employee', remove, [database])):
        menu.append_item(item)
    menu.show()
