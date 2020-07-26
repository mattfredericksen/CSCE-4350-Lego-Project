from sql import LegoDB


def view(database: LegoDB):
    print('VIEWING STORES\n')

    for store_id, address, *_ in database.get_stores():
        print(f'(ID: {store_id}) - {address}')

    input('\nPress [enter] to return.')


def create(database: LegoDB):
    print('CREATING NEW STORE\n'
          '[entering a blank field cancels this process]\n')

    address = input('Store address: ')
    if not address:
        return

    while True:
        manager_id = input('Manager\'s employee ID [0 for no manager]: ')
        try:
            manager_id = int(manager_id)
        except ValueError:
            if manager_id == '':
                return
            print(f'\nInvalid employee ID: "{manager_id}"')
            continue
        else:
            if manager_id and database.get_employees(manager_id):
                print(f'\nInvalid employee ID: "{manager_id}"')
                continue
            break
    try:
        database.create_store(address, manager_id)
    except Exception as e:
        print(f'\n{e}')
        input('Failed to create store. Press [enter].')
        return

    input('Store created.\n'
          'Press [enter] to return.')


def remove(database: LegoDB):
    pass
