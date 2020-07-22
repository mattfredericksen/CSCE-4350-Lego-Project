from consolemenu import ConsoleMenu
from consolemenu.items import FunctionItem

from .details import details
from .sale import print_sale

from test_data.static import sets, bricks


def select_payment(context: dict):
    input('Select payment method')


def checkout(context: dict):
    items = [(i, f'(Qty: {q}) {sets[i]["name"]}')
             for i, q in context['cart']['sets'].items()] + \
            [(i, f'(Qty: {q}) {bricks[i]["description"]}')
             for i, q in context['cart']['bricks'].items()]

    instructions = 'Select an item to modify its quantity.'
    menu = ConsoleMenu('Checkout', exit_option_text='Return to Main Menu',
                       prologue_text=instructions,
                       epilogue_text=instructions)

    for i, q in context['cart']['sets'].items():
        menu.append_item(FunctionItem(f'(Qty: {q}) {sets[i]["name"]}',
                                      details, [context, i, 'Set'],
                                      should_exit=True))
    for i, q in context['cart']['bricks'].items():
        menu.append_item(FunctionItem(f'(Qty: {q}) {bricks[i]["name"]}',
                                      details, [context, i, 'Brick'],
                                      should_exit=True))

    continue_item = FunctionItem('Continue to View Totals', print_sale,
                                 [context, context['cart'], 'CART TOTALS',
                                  'Continue to Payment Method? [y/n]: '],
                                 should_exit=True)
    menu.append_item(continue_item)

    while True:
        menu.show()
        if (menu_item := menu.selected_item) is menu.exit_item:
            return
        elif menu_item is continue_item:
            if menu.returned_value in ('y', 'ye', 'yes'):
                select_payment(context)
                return
        elif (qty := menu.returned_value) is None:
            continue
        elif qty is 0:
            menu.remove_item(menu_item)
        else:
            menu_item.text = f'(Qty: {qty}{menu_item.text[menu_item.text.find(")"):]}'
