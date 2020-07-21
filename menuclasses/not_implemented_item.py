from consolemenu.items import FunctionItem


class NotImplementedItem(FunctionItem):
    """Use this class as a placeholder when developing menu layers"""
    def __init__(self, text):
        super().__init__(text, input,
                         args=['This menu item has not been implemented yet. '
                               'Press [enter] to return.'])
