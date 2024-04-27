import tkinter as tk


class CustomButton(tk.Label):               # Création de la class qui va organiser le fonctionnement de chaque bouton
    def __init__(self, parent, event = None, parent_obj = None, func_arg = None, icons = [], *args, **kwargs) -> None:
        tk.Label.__init__(self, parent, *args, kwargs)
        
        self.kwargs = kwargs
        self.icons = icons                          # l'icône correspondante au bouton
        self.event = event                          # la fonction qui va être éxécuté lors de l'activation
        self.parent_obj = parent_obj
        self.func_arg = func_arg

        self.bind("<Enter>", self.on_enter)         # assignation des touches permettant d'interagir avec le programme
        self.bind("<Leave>", self.on_leave)         # ...
        self.bind("<Button-1>", self.on_click)      # ...


    def on_click(self, *args):
        '''
        Fonction qui va s'éxécuter lors de l'intéraction avec le bouton (lors du click !)
        '''
        if self.event:
            self.event_generate(self.event)                                 # éxécution de la fonction après click
        
        if self.parent_obj and self.func_arg:
            self.parent_obj.passdown_func(self.func_arg)


    def on_enter(self, *args) -> None:
        '''
        Fonction qui va s'éxécuter dés lors que le curseur se trouve plus sur le bouton (changement visuel) 
        '''
        if len(self.icons) == 2:
            self.config(foreground = "#ffcc22", image = self.icons[1])      # le bouton va avoir des bordures mise en surbrillance
        self.config(foreground = "#ffcc22")


    def on_leave(self, *args) -> None:
        '''
        Fonction qui va s'éxécuter dés lors que le curseur ne se trouve plus sur le bouton (changement visuel) 
        '''
        if len(self.icons) == 2:
            self.config(foreground = "#ffcc22", image = self.icons[0])      # on retire la surbrillance des bordures du bouton
        self.config(foreground = self.kwargs.get("foreground"))