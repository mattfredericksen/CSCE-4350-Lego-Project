from consolemenu import ConsoleMenu
from consolemenu.items import FunctionItem, SubmenuItem, CommandItem
from getpass import getpass


def login():
    username = input('username: ')
    password = getpass('password: ')

    # TODO: log into SQL server
    # Assuming success:
    main_menu.show()

    # TODO: open a different menu based on capabilities of user
    #       (online mode vs store mode)


def create_account():
    username = input('new username: ')
    # TODO: select from database to confirm username is available

    password = getpass('new password: ')
    while password != getpass('confirm password: '):
        print('\npasswords do not match - try again')
        password = getpass('new password: ')

    # TODO: create normal user account in SQL database

    input('\naccount created - press [enter] to continue to The Lego Store')

    main_menu.show()


# \/\/\/\/ LOGIN MENU \/\/\/\/

login_menu = ConsoleMenu('The Lego Store', 'Please log in to continue')

login_item = FunctionItem('Login', login)
create_account_item = FunctionItem('Create Account', create_account)

login_menu.append_item(login_item)
login_menu.append_item(create_account_item)

# \/\/\/\/ MAIN MENU \/\/\/\/

main_menu = ConsoleMenu('Welcome to The Lego Store', exit_option_text='Log Out')

browse_item = FunctionItem('Browse Bricks & Sets', input, ['not yet implemented'])
order_item = FunctionItem('Place an Order', input, ['not yet implemented'])

# \/\/ account menu \/\/
account_menu = ConsoleMenu('Account Information', exit_option_text='Return to Main Menu')
account_menu_items = (FunctionItem('Change Username', input, ['not yet implemented']),
                      FunctionItem('Change Password', input, ['not yet implemented']),
                      FunctionItem('Change Email', input, ['not yet implemented']),
                      FunctionItem('Change Store Preference', input, ['not yet implemented']),
                      FunctionItem('Change Payment Options', input, ['not yet implemented']))
for item in account_menu_items:
    account_menu.append_item(item)
account_item = SubmenuItem('Account Information', account_menu, menu=main_menu)


main_menu.append_item(browse_item)
main_menu.append_item(order_item)
main_menu.append_item(account_item)

if __name__ == '__main__':
    login_menu.show()
