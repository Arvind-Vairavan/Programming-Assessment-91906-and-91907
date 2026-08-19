"""
Character Creation Window 
I dont really need version for this one since it is a simple window
"""


from tkinter import ttk, StringVar, messagebox
from gui.base_window import BaseWindow
from gui.gui_helpers import button


class CharacterCreationWindow(BaseWindow):
    
    def __init__(self, parent, game, on_complete):
        """
        Initialize the character creation window.
        """
        self.parent = parent
        self.game = game
        self.on_complete = on_complete

        super().__init__(parent, game, None, "Create Character", 500, 400)
        self._setup()
    
    def _setup(self):
        """
        Set up the user interface for character creation.
        """

        self.add_title("CREATE CHARACTER", "#00ccff")
        main = ttk.Frame(self.win, style="Dark.TFrame")
        main.pack(fill="both", expand=True, padx=30, pady=20)
        
        ttk.Label(main, text="Enter your name:", font=("Segoe UI", 12), 
                 foreground="#cccccc", background="#0a0a0a").pack(anchor="w", pady=(0, 5))
        self.name = ttk.Entry(main, font=("Segoe UI", 12), width=30)
        self.name.pack(fill="x", pady=(0, 15))
        self.name.focus()
        
        ttk.Label(main, text="Select gender:", font=("Segoe UI", 12), 
                 foreground="#cccccc", background="#0a0a0a").pack(anchor="w", pady=(0, 5))
        self.gender = StringVar(value="Male")
        f = ttk.Frame(main, style="Dark.TFrame")
        f.pack(fill="x", pady=(0, 20))
        
        for g in ["Male", "Female", "Non-binary"]:
            ttk.Radiobutton(f, text=g, variable=self.gender, value=g, 
                          style="Dark.TLabel").pack(side="left", padx=10)
        
        button(main, "START LIFE", self._create, "Green.TButton")
    
    def _create(self):
        """
        Create the character and close the window.
        """
        name = self.name.get().strip() or "Default"
        self.game.create_character(name, self.gender.get())
        self.win.destroy()
        messagebox.showinfo("Welcome!", f"Welcome, {name}!")
        self.on_complete()