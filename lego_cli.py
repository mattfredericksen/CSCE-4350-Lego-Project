from menus.login_menu import login_menu
from sql import LegoDB

credentials = {
    'host': 'localhost',
    'username': 'LegoCoApp',
    'password': 'LegoCoAppPass',
    'database': 'LegoCo'
}

if __name__ == '__main__':
    host = input('Enter database host to start the application: ')
    try:
        database = LegoDB(**credentials)
    except Exception as e:
        print('Failed to connect to database:')
        print(e)
    else:
        login_menu(database)
