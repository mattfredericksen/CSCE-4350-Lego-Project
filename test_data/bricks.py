from random import random, randint, choice


def generate_bricks():
    colors = ('red', 'orange', 'yellow', 'green',
              'blue', 'indigo', 'violet', 'white', 'black')

    return [{'id': i,
             'description': f'{randint(1,20)}x{randint(1,20)} {choice(colors)}',
             'price': round(random()*5, 2),
             'inventory': randint(0, 5)}
            for i in range(100)]
