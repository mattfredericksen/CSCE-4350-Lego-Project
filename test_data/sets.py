from random import randint, choice
from .bricks import generate_bricks
from pprint import pprint


def generate_sets():
    bricks = generate_bricks()
    brick_ids = list(bricks.keys())

    sets = {}
    for _ in range(20):
        key = randint(1, 10000)
        name = f'Set #{key}'
        description = f'Super creative description of set #{key} goes here.'
        inventory = randint(0, 5)
        set_items = {choice(brick_ids): randint(5, 15) for _ in range(randint(5, 15))}
        price = round(sum(bricks[item]['price'] * qty for item, qty in set_items.items()), 2)
        sets.update({
            key: {
                'name': name,
                'description': description,
                'inventory': inventory,
                'set_items': set_items,
                'price': price
            }
        })
    return {'sets': sets, 'bricks': bricks}


def print_set_data():
    data = generate_sets()
    pprint(data['sets'])
    print()
    pprint(data['bricks'])
