from menuclasses.selection_menu import SelectionMenuFromTuples as SelectionMenu
from sql import LegoDB


def payment_menu(database: LegoDB) -> int:
    payments = [(p_id, f'****-****-****-{card} @ {address}')
                for p_id, card, address in database.get_payments()]
    menu = SelectionMenu(payments, 'Select Payment Method',
                         subtitle='New options can be added under Account Information',
                         exit_option_text='Cancel')
    menu.show()
    return menu.selected_item.index  \
        if menu.selected_item is not menu.exit_item else 0
