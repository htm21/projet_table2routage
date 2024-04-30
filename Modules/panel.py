import tkinter as tk
import customtkinter as ctk


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
            "Backbone" : (
                load_to_size("backbone_node", *self.icon_size),
                load_to_size("backbone_node", 25, 25),
                load_to_size("backbone_node", 40, 40),
                ),
            
            "TransitOperator" : (
                load_to_size("transit_operator_node", *self.icon_size),
                load_to_size("transit_operator_node", 25, 25),
                load_to_size("transit_operator_node", 40, 40),
                ),
            
            "Operator" : (
                load_to_size("operator_node", *self.icon_size),
                load_to_size("operator_node", 25, 25),
                load_to_size("operator_node", 40, 40),
                ),
            "Connectivity" : (load_to_size("connectivity", 65, 65), load_to_size("highlight_connectivity", 65, 65)),
            "Path" : (load_to_size("path", 65, 65), load_to_size("highlight_path", 65, 65)),
            "NewNetwork" : (load_to_size("network", 65, 65), load_to_size("highlight_network", 65, 65)),
            }
        
        self.name_types = {
            "Backbone" : "BB",
            "TransitOperator" : "T-Op",
            "Operator" : "Op"
            }


        self.buffer_frame_1 = tk.Frame(self, background = "#1D2123", height = 5)
        self.buffer_frame_1.pack(side = "bottom", fill = "x")

        # Object Info ======================================================================

        self.obj_info_frame = tk.Frame(self, background = kwargs.get("background"), width = 200, height = 100)
        self.obj_info_frame.propagate(0)
        self.obj_frame = tk.Frame(self.obj_info_frame, background = kwargs.get("background"))
        self.obj_con_frame = tk.Frame(self.obj_info_frame, background = kwargs.get("background"))
        
        self.obj_label = tk.Label(self.obj_frame, compound = "top", font = f"{font} 15 bold", foreground = "#FFFFFF", background = kwargs.get("background"))
        self.bb_con = tk.Label(self.obj_con_frame, image = self.icons["Backbone"][1], compound = "left", font = f"{font} 10 bold", justify = "center", foreground = "#FFFFFF", background = kwargs.get("background"))
        self.top_con = tk.Label(self.obj_con_frame, image = self.icons["TransitOperator"][1], compound = "left", font = f"{font} 10 bold", justify = "center", foreground = "#FFFFFF", background = kwargs.get("background"))
        self.op_con = tk.Label(self.obj_con_frame, image = self.icons["Operator"][1], compound = "left", font = f"{font} 10 bold", justify = "center", foreground = "#FFFFFF", background = kwargs.get("background"))

        self.obj_info_frame.pack(side = "left", anchor = "w", fill = "x", pady = 5, padx = 20)
        self.obj_frame.pack(side = "left", fill = "both", padx = (0, 15))
        self.obj_con_frame.pack(side = "right", fill = "y")

        self.buffer_frame_1 = tk.Frame(self, background = "#1D2123", width = 5)
        self.buffer_frame_1.pack(side = "left", fill = "y", pady = 5)

        # Path Info ========================================================================

        self.path_info_frame = tk.Frame(self, background = kwargs.get("background"))
        self.path_display = tk.Canvas(self.path_info_frame, border = 0, highlightthickness = 5, background = "#171a1c", highlightbackground = "#1D2123")
        self.canvas_scroll = ctk.CTkScrollbar(self.path_info_frame, orientation = "horizontal", corner_radius = 10, hover = False, bg_color = kwargs.get("background"), command = self.path_display.xview) 
        self.path_display.config(xscrollcommand = self.canvas_scroll.set)
        
        self.path_info_frame.pack(side = "left", anchor = "w", expand = True, fill = "x", pady = 5, padx = 20)
        self.canvas_scroll.pack(side = "bottom", fill = "both", expand = True, pady = 2)
        self.path_display.pack(side = "top", fill = "x")

        # Network Tools ====================================================================

        self.network_tools = tk.Frame(self, background = kwargs.get("background"))
        self.find_path_button = CustomButton(parent = self.network_tools, parent_obj = self.app.network, func_arg = "find_path", icons = self.icons["Path"], image = self.icons["Path"][0], background = "#22282a")
        self.connectivity_button = CustomButton(parent = self.network_tools, parent_obj = self.app.network, func_arg = "check_connectivity", icons = self.icons["Connectivity"], image = self.icons["Connectivity"][0], background = "#22282a")
        self.generate_network = CustomButton(parent = self.network_tools, parent_obj = self.app.network, func_arg = "generate_network", icons = self.icons["NewNetwork"], image = self.icons["NewNetwork"][0], background = "#22282a")

        self.network_tools.pack(side = "right", padx = 20)
        self.generate_network.pack(side = "right", padx = 15)
        self.connectivity_button.pack(side = "right", padx = 15)
        self.find_path_button.pack(side = "right", padx = 15)

        self.buffer_frame_2 = tk.Frame(self, background = "#1D2123", width = 5)
        self.buffer_frame_2.pack(side = "right", fill = "y", pady = 5)

    # GUI Functions ====================================================================\


    def set_path_info(self, path : list[Node], weight : int) -> None:
        self.path_display.delete("obj")

        node_offset = 300
        node_canvas_ids = []
        
        self.path_display.create_text(50, 20, anchor = "w", text = f"Path Weight : {weight}", fill = "white", font = f"{font} 12 bold", tags = "obj")
        self.path_display.create_text(50, 45, anchor = "w", text = f"Path Length : {len(path)}", fill = "white", font = f"{font} 12 bold", tags = "obj")
        
        for index, node in enumerate(path):
            if index == 0:
                node_canvas_id = self.path_display.create_image(node_offset, 30, anchor = "center", image = self.icons[node.type][2], tags = ["obj", "node"]) 
                self.path_display.create_text(node_offset, 58, text = f"{self.name_types[node.type]} {node.id}", fill = "white", font = f"{font} 12 bold", tags = "obj")
            else:  
                node_canvas_id = self.path_display.create_image(node_offset, 30, anchor = "center", image = self.icons[node.type][2], tags = ["obj", "node"]) 
                self.path_display.create_text(node_offset, 60, text = f"{self.name_types[node.type]} {node.id}", fill = "white", font = f"{font} 12 bold", tags = "obj")
            node_offset += 100
            node_canvas_ids.append(node_canvas_id)

        for index in range(len(node_canvas_ids) - 1):
            node_1_coords : tuple = self.path_display.coords(node_canvas_ids[index])
            node_2_coords : tuple = self.path_display.coords(node_canvas_ids[index + 1])
            self.path_display.create_line((*node_1_coords, *node_2_coords), width = 5, fill = "#22282a", smooth = True, tags = ["obj", "connection"])


        self.path_display.tag_raise("node")



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
            self.obj_label.config(image = self.icons[obj.type][0], text = f"{self.name_types[node.type]} {node.id}")
            self.bb_con.config(text = f" {node.backbone_connections}")
            self.top_con.config(text = f" {node.transit_opertator_connections}")
            self.op_con.config(text = f" {node.opertator_connections}")

            self.bb_con.pack(side = "top", expand = True)
            self.top_con.pack(side = "top", expand = True)
            self.op_con.pack(side = "top", expand = True)