from consolemenu import ConsoleMenu, SelectionMenu
from consolemenu.items import FunctionItem, SubmenuItem, SelectionItem
from consolemenu.menu_formatter import MenuFormatBuilder
from consolemenu.menu_component import Dimension

from .not_implemented_item import NotImplementedItem

from test_data.bricks import generate_bricks

# TODO: Think about how we want to implement orders.
#       Perhaps when an item is selected for more details,
#       we can show an 'add to cart' option with qty input.
#       Do we want a 'shopping cart' menu instead of 'Place an Order'?


class SelectionMenuFromTuples(SelectionMenu):
    def __init__(self, tuples, title=None, subtitle=None, screen=None, formatter=None,
                 prologue_text=None, epilogue_text=None, show_exit_option=True, exit_option_text='Exit'):
        super(SelectionMenu, self).__init__(title, subtitle, screen=screen, formatter=formatter,
                                            prologue_text=prologue_text, epilogue_text=epilogue_text,
                                            show_exit_option=show_exit_option, exit_option_text=exit_option_text)
        for index, item in tuples:
            self.append_item(SelectionItem(item, index, self))


def browse_bricks():
    description = 'Select an item to view more details or '  \
                  'to add it to your cart'
    bricks = [(brick['id'], brick['description']) for brick in generate_bricks()]
    dimension = Dimension(width=max(50, max(len(brick[1]) for brick in bricks) + 18))
    formatter = MenuFormatBuilder(max_dimension=dimension)
    browser = SelectionMenuFromTuples(bricks, title='Browse Bricks',
                                      formatter=formatter,
                                      prologue_text=description,
                                      epilogue_text=description)
    browser.show()
    input(f'You selected: {browser.selected_item.text}\nPress [enter] to exit.')


browse_menu = ConsoleMenu('Browse LEGO Products',
                          exit_option_text='Return to Main Menu')

for item in (FunctionItem('Browse Bricks', browse_bricks),
             NotImplementedItem('Browse Sets'),
             NotImplementedItem('Browse All'),
             NotImplementedItem('Search All')):
    browse_menu.append_item(item)
