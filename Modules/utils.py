import os
import platform
import tkinter as tk

from random import randint
from PIL import Image,ImageTk
from Modules.node import *


app_folder_path = os.getcwd().replace("\\", "/")
font = "Montserrat" if platform.system() == "Windows" else "Arial"


NODE_TYPE : dict[str : Node] = {                                                # Dictionnaire qui relie chaque type (string) à leur class respective
    "Tier1" : Tier1,
    "Tier2" : Tier2,
    "Tier3" : Tier3,
    "Node" : Node
}

ALERTS = {
    "Success": {

        },
    
    "Error" : {

        }
    }

def screen_dimensions(root : tk.Tk) -> tuple[int, int]:
    ''' Fonction qui retourne les dimensions de l'interface graphique '''
    return root.winfo_screenwidth(), root.winfo_screenheight()                  # respectivement largeur, hauteur


def load_to_size(icon : str, width : int, height : int) -> ImageTk.PhotoImage:
    ''' Fonction qui permet l'importation des icones (du dossier Icons) dans l'interface graphiques '''
    icon = Image.open(f"{app_folder_path}/Icons/{icon}.png")
    icon = icon.resize((width, height))

    return ImageTk.PhotoImage(icon)


def set_node_boundries(c_width, c_height) -> None:
    boundries = {
        "Backbone" : {"width" : None, "height" : None}, # 30% screen from center
        "TransitOperator" : {"width" : None, "height" : None}, # 20% screen form "Backbone" min width & height
        "Operator" : {"width" : None, "height" : None}, # 20% screen form "TransitOperator" min width & height
        }

    bb_width_pcent, bb_height_pcent = (c_width * 30) // 100, (c_height * 30) // 100    
    bb_width_min, bb_width_max = c_width - bb_width_pcent, c_width + bb_width_pcent
    bb_height_min, bb_height_max = c_height - bb_height_pcent, c_height + bb_height_pcent

    t_op_width_pcent, t_op_height_pcent = (c_width * 20) // 100, (c_height * 20) // 100
    t_op_width_min, t_op_width_max = bb_width_min - t_op_width_pcent, bb_width_max + t_op_width_pcent
    t_op_height_min, t_op_height_max = bb_height_min - t_op_height_pcent, bb_height_max + t_op_height_pcent

    op_width_pcent, op_height_pcent = (c_width * 20) // 100, (c_height * 20) // 100
    op_width_min, op_width_max = t_op_width_min - op_width_pcent, t_op_width_max + op_width_pcent
    op_height_min, op_height_max = t_op_height_min - op_height_pcent, t_op_height_max + op_height_pcent

    boundries["Backbone"]["width"] = (bb_width_min, bb_width_max)
    boundries["Backbone"]["height"] = (bb_height_min, bb_height_max)
    
    boundries["TransitOperator"]["width"] = (t_op_width_min, t_op_width_max)
    boundries["TransitOperator"]["height"] = (t_op_height_min, t_op_height_max)
    
    boundries["Operator"]["width"] = (op_width_min, op_width_max)
    boundries["Operator"]["height"] = (op_height_min, op_height_max)

    return boundries


def choose_coords(boundries : dict, specific : str) -> tuple:
    
    x, y = randint(*boundries[specific]["width"]), randint(*boundries[specific]["height"])
    valid = False
    
    if specific == "TransitOperator":

        while not valid:
            if x > boundries["Backbone"]["width"][0] and x < boundries["Backbone"]["width"][1] and y < boundries["Backbone"]["height"][0] or y > boundries["Backbone"]["height"][1]:
                valid = True
            elif x < boundries["Backbone"]["width"][0] or x > boundries["Backbone"]["width"][1] and y > boundries["Backbone"]["height"][0] and y < boundries["Backbone"]["height"][1]:
                valid = True
            else:
                x = randint(*boundries["TransitOperator"]["width"])
                y = randint(*boundries["TransitOperator"]["height"])

    elif specific == "Operator":
        while not valid:
            if x > boundries["TransitOperator"]["width"][0] and x < boundries["TransitOperator"]["width"][1] and y < boundries["TransitOperator"]["height"][0] or y > boundries["TransitOperator"]["height"][1]:
                valid = True
            elif x < boundries["TransitOperator"]["width"][0] or x > boundries["TransitOperator"]["width"][1] and y > boundries["TransitOperator"]["height"][0] and y < boundries["TransitOperator"]["height"][1]:
                valid = True
            else:
                x = randint(*boundries["Operator"]["width"])
                y = randint(*boundries["Operator"]["height"])
        
    
    return x, y
