from menus.login_menu import login_menu
from sql import LegoDB

credentials = {
    'host': 'localhost',
    'username': 'LegoCoApp',
    'password': 'LegoCoAppPass',
    'database': 'LegoCo'
}

if __name__ == '__main__':
    try:
        database = LegoDB(**credentials)
    except Exception as e:
        print('Failed to connect to database:')
        print(e)
        print('Try again manually.')
        host = input('Host: ')
        username = input('Username (LegoCoApp): ')
        password = input('Password (LegoCoAppPass): ')
        database = input('Database (LegoCo): ')
        try:
            database = LegoDB(host, username, password, database)
        except Exception as e:
            print(e)
            input('Failed again. Press [enter] to exit.')
        else:
            login_menu(database)
    else:
        login_menu(database)
