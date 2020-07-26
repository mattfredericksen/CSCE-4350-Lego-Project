from consolemenu import ConsoleMenu
from consolemenu.items import FunctionItem

from menuclasses.not_implemented_item import NotImplementedItem
from menufunctions.reports import *

from sql import LegoDB


def report_menu(database: LegoDB):
    menu = ConsoleMenu('Report Menu', 'Select a report to generate.',
                       exit_option_text='Return to Main Menu')
    for item in (
             # count, total price, average order total
             FunctionItem('Online Orders', online_orders, [database]),
             # count of cancellations grouped by year/month
             FunctionItem('Online Order Cancellations', orders_cancellations, [database]),
             # count, total price, average sale total, sales per employee
             NotImplementedItem('NYI: Store Sales'),
             # count, total return price
             NotImplementedItem('NYI: Store Returns'),
             # across orders and sales
             FunctionItem('Best Selling Items', best_selling, [database]),
             # across orders and sales
             FunctionItem('Most Returned Items', most_returned, [database]),
             # items with stock below specified threshold
             NotImplementedItem('NYI: Inventory')):
        menu.append_item(item)
    menu.show()
