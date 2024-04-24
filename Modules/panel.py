import tkinter as tk

from Modules.utils import *


class Panel(tk.Frame):

    def __init__(self, parent : tk.Widget, app : object, *args : tuple, **kwargs : dict) -> None: 
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.app = app
        self.parent : tk.Frame = parent
        self.kwargs = kwargs

        self.icon_size = 75, 75
        self.icons = {
            "Network" : load_to_size("network", *self.icon_size),
            "Backbone" : load_to_size("backbone_node", *self.icon_size),
            "TransitOperator" : load_to_size("transit_operator_node", *self.icon_size),
            "Operator" : load_to_size("operator_node", *self.icon_size)
            }
        

        self.buffer_frame = tk.Frame(self, background = "#1D2123", height = "5")
        self.buffer_frame.pack(side = "bottom", fill = "x")