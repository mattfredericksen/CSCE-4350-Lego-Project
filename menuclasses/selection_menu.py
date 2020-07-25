from consolemenu import SelectionMenu
from consolemenu.items import SelectionItem
from consolemenu.menu_formatter import MenuFormatBuilder
from consolemenu.menu_component import Dimension
from os import get_terminal_size


class SelectionMenuFromTuples(SelectionMenu):
    """Used for manually providing indexes to list items

    This class is useful since we often want a meaningful
    item id returned from the selection menu.
    """

    # partially copied from SelectionMenu's __init__()
    def __init__(self, tuples, title=None, subtitle=None, screen=None, formatter=None,
                 prologue_text=None, epilogue_text=None, show_exit_option=True, exit_option_text='Exit'):

        # menu width is at least 80 expanding as necessary to fit strings
        # this expansion halts at terminal width
        if tuples and not formatter:
            width = min(get_terminal_size().columns, max(80, max(len(item[1]) for item in tuples) + 18))
            dimension = Dimension(width=width)
            formatter = MenuFormatBuilder(max_dimension=dimension)

        super(SelectionMenu, self).__init__(title, subtitle, screen=screen, formatter=formatter,
                                            prologue_text=prologue_text, epilogue_text=epilogue_text,
                                            show_exit_option=show_exit_option, exit_option_text=exit_option_text)
        for index, item in tuples:
            self.append_item(SelectionItem(item, index, self))