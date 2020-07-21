from menuclasses.selection_menu import SelectionMenuFromTuples
from getpass import getpass

from test_data.static import employees, stores


def view(context: dict):
    # TODO: set to show employees in current store only
    print(f'EMPLOYEES OF STORE #{context["store"]}\n')
    manager = stores[context['store']]['manager']
    emps = ((eid, e['name']) for eid, e in employees.items() if e['store'] == context['store'])
    for eid, name in emps:
        print(f'Employee ID: {eid}\n'
              f'\tName: {name}\n'
              f'\tPosition: {"Manager" if eid is manager else "Grunt"}\n')

    input('\nPress [enter] to return.')


def create(context: dict):
    print(f'CREATE EMPLOYEE IN STORE #{context["store"]}\n')

    name = input("New employee name: ")
    username = input('New employee username: ')
    password = getpass('New employee password: ')

    # TODO: SQL insert

    input('\nEmployee has been created.\n'
          'Press [enter] to return.')


def remove(context: dict):
    print('REMOVE EMPLOYEE IN STORE #{store_id}\n')
    emps = tuple((eid, f'(ID: {eid}) {e["name"]}')
                 for eid, e in employees.items() if e['store'] == context['store'])
    menu = SelectionMenuFromTuples(emps, 'REMOVE EMPLOYEE',
                                   exit_option_text='Cancel')
    menu.show()
    if menu.selected_item is not menu.exit_item:
        employees[menu.selected_item.index]['active'] = False

    # TODO: SQL modify

    print('EMPLOYEE REMOVED:\n'
          f'\t{menu.selected_item.text}\n')
    input('Press [enter] to return.')
