import ctypes
import platform
import tkinter as tk
import random as rd

from time import time
from Modules.app import App


def main() -> None:

    # Ignore la mise à l'échelle de l'écran des machines Windows pour que les widgets de l'interface graphique n'apparaissent pas trop gros à l'écran.
    # C'est surtout pour les widgets qui contiennent du texte.
    if platform.system() == "Windows":
        ctypes.windll.shcore.SetProcessDpiAwareness(0)


    # Ici, nous initialisons la fenêtre tkinter (interface graphique) et la passons en entrée d'une instance de la classe App où elle sera gérée. 
    root = tk.Tk()
    app  = App(root)


    # app.Running est défini à "True" au démarrage et arrêtera toutes les mises à jour et fonctions de l'interface graphique et de la logique s'il est défini à "False".
    while app.Running:

        # la déclaration try-else permet de détecter les éventuels bugs :)
        try:  
            if app.alert_lable.winfo_ismapped():
                if (time() - app.alert_create_time) > app.alert_on_screen_time:
                    app.alert_lable.place_forget()
        except: 
            pass
        
        # Utilisation de update au lieu de mainloop pour ne pas rester bloqué dans une boucle
        root.update()



if __name__ == "__main__" :
    # On nettoie le terminal au démarrage
    print("\033c")
    main()

