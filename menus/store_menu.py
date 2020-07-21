from consolemenu import ConsoleMenu
from consolemenu.items import FunctionItem
from menuclasses.not_implemented_item import NotImplementedItem

from test_data.static import stores, employees


def view(context: dict):
    print('VIEWING STORES\n')

    for store_id, store in stores.items():
        # currently assumes that all stores have managers
        # manager = employees[store["manager"]]["name"] if store["manager"] else None
        count = len([e for e in employees.values() if e['store'] == store_id])
        print(f'Store ID: {store_id}:\n'
              f'\tAddress: {store["address"]}\n'
              f'\tManager: {employees[store["manager"]]["name"]}\n'
              f'\tEmployee Count: {count}\n')

    input('Press [enter] to return.')


def create(context: dict):
    print('CREATING NEW STORE\n'
          '[entering a blank field cancels this process]\n')

    address = input('Store address: ')
    if not address:
        return

    manager_id = None
    while True:
        manager_id = input('Manager\'s employee ID: ')
        try:
            manager_id = int(manager_id)
        except ValueError:
            if manager_id == '':
                return
        else:
            if manager_id in employees:
                break
        print(f'\nInvalid employee ID: "{manager_id}"')

    # TODO: run SQL to insert new store

    input('Store created.\n'
          'Press [enter] to return.')


def store_menu(context: dict):
    menu = ConsoleMenu('Store Management', exit_option_text='Return to Main Menu')
    for item in (FunctionItem('View Stores', view, (context,)),
                 FunctionItem('Create Store', create, (context,)),
                 NotImplementedItem('Remove Store')):
        menu.append_item(item)
    menu.show()
