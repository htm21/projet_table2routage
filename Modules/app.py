import pyglet
import platform
import tkinter as tk

from time import time
from Modules.panel import *
from Modules.network import *
from Modules.utils import *

class App(object):

    if platform.system() == "Windows":
        pyglet.font.add_file(f"{app_folder_path}/Font/{font}.ttf")

    def __init__(self, parent : tk.Tk) -> None:
        
        self.parent = parent
        self.Running = True
        self.update_speed = 1

        self.icon_size = 15, 15
        self.icons = {
            "Success" : load_to_size("success", *self.icon_size),
            "Error" : load_to_size("error", *self.icon_size)
            }

        self.alert = None
        self.alert_on_screen_time = 5
        self.alert_create_time = 0


        # Window Positioning ===========================================================

        screen_w, screen_h = screen_dimensions(self.parent)
        screen_w_center, screen_h_center = screen_w // 2, screen_h // 2
        
        self.gui_w, self.gui_h = 1600, 900
        self.gui_w_center, self.gui_h_center = self.gui_w // 2, (self.gui_h // 2) + 20
        self.x, self.y = screen_w_center - self.gui_w_center, screen_h_center - self.gui_h_center

        # Window Settings ==============================================================

        self.parent.geometry(f"{self.gui_w}x{self.gui_h}+{self.x}+{self.y}")      
        self.parent.title("Project Table Routage")
        self.parent.resizable(False, False)
        self.parent.update()

        # Frames =======================================================================

        self.MAIN_FRAME = tk.Frame(self.parent, background = "#FFFFFF", highlightthickness = 5, highlightbackground = "#1D2123", highlightcolor = "#1D2123")
        self.MAIN_FRAME.pack(anchor = "center", fill = "both", expand = True)
        
        self.info_panel = Panel(self.MAIN_FRAME, app = self, background = "#22282a", height = 125)
        self.info_panel.pack_propagate(0)

        self.network = Network(self.MAIN_FRAME, app = self, border = 0, highlightthickness = 0, background = "#171a1c")
        self.network.pack(side = "bottom", fill = "both", expand = True)

        # Widgets ======================================================================

        self.alert_lable = tk.Label(self.parent, compound = "left", font = f"{font} 15 bold", foreground = "#FFFFFF", padx = 10)

        # Binds ========================================================================

        self.parent.bind("<<Alert>>", self.create_alert)
        self.parent.protocol("WM_DELETE_WINDOW", self.on_closing)


    def on_closing(self, *args) -> None:
        self.Running = False

    def create_alert(self, *args) -> None:
        text = " " + ALERTS[self.alert[0]][self.alert[1]]
        color = "#4d0000" if self.alert[0] == "Error" else "#004d00"

        self.alert_lable.config(image = self.icons[self.alert[0]], text = text, font = f"{font} 15 bold", foreground = "#FFFFFF", background = color)
        self.alert_create_time = time()
        self.alert_lable.place(anchor = "sw", relx = 0, rely = 1, bordermode = "inside")




