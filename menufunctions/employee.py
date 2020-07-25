from menuclasses.selection_menu import SelectionMenuFromTuples
from getpass import getpass

from sql import LegoDB


def view(database: LegoDB):
    emp_by_store = {}
    for e_id, name, store_id in database.get_employees():
        emp_by_store.setdefault(store_id, []).append((e_id, name))
    print(f'EMPLOYEES BY STORE\n')
    for store_id, e_list in emp_by_store.items():
        print(f'Store {store_id} ({database.get_stores(store_id)[1]})')
        for e_id, name in e_list:
            print(f'\t(ID: {e_id}) - {name}')
        print()
    input('\nPress [enter] to return.')


def create(database: LegoDB):
    print('CREATE EMPLOYEE\n')
    name = input("New employee name: ")
    username = input('New employee username: ')
    password = getpass('New employee password: ')
    store = input('Store ID: ')

    try:
        database.create_employee(name, username, password, store)
    except Exception as e:
        print(f'\n{e}')
        input('Unable to create employee.\n'
              'Press [enter] to return.')
    else:
        input('\nEmployee has been created.\n'
              'Press [enter] to return.')


def remove(database: LegoDB):
    """Employees are disabled, not deleted, to maintain dB integrity"""
    print('REMOVE EMPLOYEE\n')
    try:
        database.disable_employee(int(input('Employee ID to disable: ')))
    except Exception as e:
        print(f'\n{e}')
        input('Unable to disable employee account. Press [enter].')
    else:
        input('Employee will now be unable to sign in. Press [enter].')
