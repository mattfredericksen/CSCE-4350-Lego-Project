from sql import LegoDB


def online_orders(database: LegoDB):
    report = database.orders_report()
    print('REPORT - ONLINE ORDERS\n')
    print(f'Number of orders: {report["order_count"]}\n'
          f'Total price of orders: ${report["order_total"]:,.2f}\n'
          f'Average price of orders: ${report["average_price"]:,.2f}\n\n'
          f'Total number of bricks: {report["brick_count"]}\n'
          f'Average number of bricks: {report["brick_average"]}\n\n'
          f'Total number of sets: {report["set_count"]}\n'
          f'Average number of sets: {report["set_average"]}\n')

    input('Press [enter] to return.')


def orders_cancellations(database: LegoDB):
    report = database.cancellations_report()
    print('REPORT - ONLINE CANCELLATIONS\n')
    print(f'Total number of cancellations: {report[0]}\n'
          f'Total price of cancellations: {report[1]}\n')

    input('Press [enter] to return.')


def best_selling(database: LegoDB):
    report = database.best_selling_report()
    print('REPORT - BEST SELLING ITEMS\n')
    print('Sets:')
    for set_id, name, quantity in report['sets']:
        print(f'\tID: {set_id}, Name: "{name}", Quantity sold: {quantity})')
    print('Bricks:')
    for brick_id, description, quantity in report['bricks']:
        print(f'\tID: {brick_id}, Name: "{description}", Quantity sold: {quantity})')
    input('\nPress [enter] to return.')


def most_returned(database: LegoDB):
    report = database.most_returned_report()
    print('REPORT - MOST RETURNED ITEMS\n')
    print('Sets:')
    for set_id, name, quantity in report['sets']:
        print(f'\tID: {set_id}, Name: "{name}", Quantity returned: {quantity})')
    print('Bricks:')
    for brick_id, description, quantity in report['bricks']:
        print(f'\tID: {brick_id}, Name: "{description}", Quantity returned: {quantity})')
    input('\nPress [enter] to return.')
