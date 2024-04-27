import tkinter as tk

from Modules.network import *
from Modules.utils import *


class Panel(tk.Frame):

    def __init__(self, parent : tk.Widget, app : object, *args : tuple, **kwargs : dict) -> None: 
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.app = app
        self.parent : tk.Frame = parent
        self.kwargs = kwargs

        self.icon_size = 65, 65
        self.icons = {
            "Network" : load_to_size("network", *self.icon_size),
            "Backbone" : load_to_size("backbone_node", *self.icon_size),
            "TransitOperator" : load_to_size("transit_operator_node", *self.icon_size),
            "Operator" : load_to_size("operator_node", *self.icon_size),
            "BackboneCon" : load_to_size("backbone_node", 25, 25),
            "TransitOperatorCon" : load_to_size("transit_operator_node", 25, 25),
            "OperatorCon" : load_to_size("operator_node", 25, 25)
            }


        self.buffer_frame_1 = tk.Frame(self, background = "#1D2123", height = 5)
        self.buffer_frame_1.pack(side = "bottom", fill = "x")

        self.obj_info_frame = tk.Frame(self, background = kwargs.get("background"))
        self.obj_frame = tk.Frame(self.obj_info_frame, background = kwargs.get("background"))
        self.obj_con_frame = tk.Frame(self.obj_info_frame, background = kwargs.get("background"))
        
        self.obj_label = tk.Label(self.obj_frame, compound = "top", font = f"{font} 15 bold", justify = "left", foreground = "#FFFFFF", background = kwargs.get("background"))
        self.bb_con = tk.Label(self.obj_con_frame, image = self.icons["BackboneCon"], compound = "left", font = f"{font} 8 bold", justify = "center", foreground = "#FFFFFF", background = kwargs.get("background"))
        self.top_con = tk.Label(self.obj_con_frame, image = self.icons["TransitOperatorCon"], compound = "left", font = f"{font} 8 bold", justify = "center", foreground = "#FFFFFF", background = kwargs.get("background"))
        self.op_con = tk.Label(self.obj_con_frame, image = self.icons["OperatorCon"], compound = "left", font = f"{font} 8 bold", justify = "center", foreground = "#FFFFFF", background = kwargs.get("background"))

        self.obj_info_frame.pack(side = "left", anchor = "w", fill = "x", pady = 15)
        self.obj_frame.pack(side = "left", fill = "y", padx = (0, 15))
        self.obj_con_frame.pack(side = "left", fill = "y")




    def set_object_info(self, obj : object) -> None:
        
        self.obj_label.pack(side = "top")

        if isinstance(obj, Network):
            network : Network = obj
            self.obj_label.config(image = self.icons["Network"], text = "Network")
            self.bb_con.config(text = f" {len(network.tier1_nodes)}")
            self.top_con.config(text = f" {len(network.tier2_nodes)}")
            self.op_con.config(text = f" {len(network.tier3_nodes)}")

            self.bb_con.pack(side = "top", expand = True)
            self.top_con.pack(side = "top", expand = True)
            self.op_con.pack(side = "top", expand = True)
    
        elif isinstance(obj, Node):
            node : Node = obj
            self.obj_label.config(image = self.icons[obj.type] , text = node.name)
            self.bb_con.config(text = f" {node.backbone_connections}")
            self.top_con.config(text = f" {node.transit_opertator_connections}")
            self.op_con.config(text = f" {node.opertator_connections}")

            self.bb_con.pack(side = "top", expand = True)
            self.top_con.pack(side = "top", expand = True)
            self.op_con.pack(side = "top", expand = True)