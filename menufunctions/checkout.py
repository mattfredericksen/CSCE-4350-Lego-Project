from .sale import print_sale
from menuclasses.selection_menu import SelectionMenuFromTuples


def checkout(context: dict):
    print_sale(context, context['cart'], 'CART ITEMS')

    if input('\nContinue to checkout? [y/n]: ').lower() not in ('y', 'yes'):
        return

    # Create a SelectionMenuFromTuples for each payment option
    # the user has. Add an option for adding a new payment option.

    # Once the user has selected a payment option, SQL happens
    # Cart item in Order table gets modified,
    # and inventory of store is modified.
