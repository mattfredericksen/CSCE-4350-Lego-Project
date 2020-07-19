from random import randint, choice
from .bricks import generate_bricks


def generate_sets():
    bricks = generate_bricks()
    brick_ids = list(bricks.keys())

    sets = {}
    for _ in range(1, 20):
        key = randint(1, 10000)
        name = f'Set #{key}'
        description = 'Super creative description goes here'
        items = {choice(brick_ids): randint(5, 15) for _ in range(5, 15)}
        price = round(sum(bricks[item]['price'] * qty for item, qty in items.items()), 2)
        sets.update({
            key: {
                'name': name,
                'description': description,
                'set_items': items,
                'price': price
            }
        })
    return {'sets': sets, 'bricks': bricks}
