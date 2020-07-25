"""This menu is shown when customers select "Account Information"."""

from consolemenu import ConsoleMenu
from consolemenu.items import FunctionItem
from menuclasses.not_implemented_item import NotImplementedItem

from sql import LegoDB


def add_payment_option(database: LegoDB):
    print('NEW PAYMENT OPTION')
    print('Enter nothing in a field to cancel.\n')

    while len(card := input('Card number: ')) != 16:
        if not card:
            return
        print('Invalid number length\n')
    while len(exp_date := input('Expiration date [YYYY-MM]: ')) != 7:
        if not exp_date:
            return
        print('Invalid date\n')
    address = input('Billing address: ')
    if not address:
        return

    try:
        database.add_payment_option(card, f'{exp_date}-01', address)
    except Exception as e:
        print(f'\n{e}')
        input('Failed to add payment option. Press [enter] to return.')
    else:
        input('Success. Press [enter] to return.')


def change_store_preference(database: LegoDB):
    menu = ConsoleMenu('Select Preferred Store',
                       f'Current store: {database.get_stores(database.get_store_preference())}',
                       exit_option_text='Return')
    for store_id, address in database.get_stores():
        menu.append_item(
            FunctionItem(address, database.set_store_preference,
                         [store_id], should_exit=True))
    menu.show()
    input('Success. Press [enter] to return.')


def change_shipping_address(database: LegoDB):
    print('CHANGE SHIPPING ADDRESS\n'
          'Enter nothing to cancel.\n\n'
          f'Current address: {database.get_shipping_address()}\n')

    if not (address := input('Shipping address: ')):
        return
    try:
        database.set_shipping_address(address)
    except Exception as e:
        print(f'\n{e}')
        input('Failed to change address. Press [enter] to return.')
    else:
        input('Success. Press [enter] to return.')


def account_menu(database: LegoDB):
    menu = ConsoleMenu('Account Information', exit_option_text='Return to Main Menu')
    for item in (NotImplementedItem('NYI: Change Username'),
                 NotImplementedItem('NYI: Change Password'),
                 NotImplementedItem('NYI: Change Email'),
                 FunctionItem('Add Payment Option', add_payment_option, [database]),
                 FunctionItem('Change Shipping Address', change_shipping_address, [database]),
                 FunctionItem('Change Store Preference', change_store_preference, [database])):
        menu.append_item(item)
    menu.show()
