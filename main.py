import ctypes
import platform
import tkinter as tk
import random as rd

from time import time
from Modules.app import App


def main() -> None:

    # Ignores Windows Screen Scaling so the GUI widgets don't look blown out on screen
    # This is mostly for any widgets that contain text
    if platform.system() == "Windows":
        ctypes.windll.shcore.SetProcessDpiAwareness(0)


    # Here we initialize the tkinter window and pass it onto the App class where it will be managed 
    root = tk.Tk()
    app  = App(root)


    # app.Running is set to "True" at start and will stop all GUI & Logic updates and functions when set to "False"
    while app.Running:

        # try-else statement to catch any bugs
        try:  
            if app.alert_lable.winfo_ismapped():
                if (time() - app.alert_create_time) > app.alert_on_screen_time:
                    app.alert_lable.place_forget()
        except: 
            pass
        
        # Use of update instead of mainloop to not get stuck in a loop
        root.update()



if __name__ == "__main__" :
    # Clear Terminal at Start (for debug)
    print("\033c")
    main()

