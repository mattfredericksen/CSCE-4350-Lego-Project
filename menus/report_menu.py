from consolemenu import ConsoleMenu
from consolemenu.items import FunctionItem

from menuclasses.not_implemented_item import NotImplementedItem


def report_menu(context: dict):
    menu = ConsoleMenu('Report Menu', 'Select a report to generate.',
                       exit_option_text='Return to Main Menu')
    for item in (
             # count, total price, average order total
             NotImplementedItem('Online Orders'),
             # count of cancellations grouped by year/month
             NotImplementedItem('Online Order Cancellations'),
             # count, total price, average sale total, sales per employee
             NotImplementedItem('Store Sales'),
             # count, total return price, returns per employee
             NotImplementedItem('Store Returns'),
             # across orders and sales
             NotImplementedItem('Highest Selling Items'),
             # across orders and sales
             NotImplementedItem('Most Returned Items'),
             # items with stock below specified threshold
             NotImplementedItem('Inventory')):
        menu.append_item(item)
    menu.show()
