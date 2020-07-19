from random import uniform, randint, choice


def generate_bricks():
    colors = ('red', 'orange', 'yellow', 'green',
              'blue', 'indigo', 'violet', 'white', 'black')

    return {randint(1, 10000):
            {'description': f'{randint(1,20)}x{randint(1,20)} {choice(colors)}',
             'price': round(uniform(.1, 2), 2),
             'inventory': randint(0, 5)}
            for _ in range(1, 100)}
