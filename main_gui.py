"""
Version 1 of Main gui 
this version has quite a few bug and other things that could be done better

I have listed them throughout the code and hopefully I will be fixing them in the next version 
"""

from tkinter import Tk, ttk, messagebox


class BitLifeGUI:
    """
    Main GUI window for BitLife game.
    
    BUG: Window size may cut off content on smaller screens
    BUG: Stats label may overflow with long text
    BUG: No validation for missing child windows
    BUG: Age up doesn't check for death conditions properly
    """
    
    def __init__(self, root):
        """
        Initialize the main GUI.
        
        BUG: Root window not configured for proper resizing
        BUG: Game instance created but not properly initialized
        """
        self.root = root
        self.root.title("BitLife")
        self.root.geometry("1400x1000")  # BUG: Fixed size may not fit all screens
        self.root.minsize(900, 700)
        self.root.configure(bg="#0a0a0a")

        from logic.game import Game
        self.game = Game()  # BUG: No error handling if Game fails to load

        self._setup_styles()
        self._setup_ui()
        self.update_display()

    def _setup_styles(self):
        """
        Setup ttk styles.
        
        BUG: Styles not properly applied to all widgets
        BUG: Colors may not be visible on all displays
        """
        style = ttk.Style()
        style.theme_use("clam")

        colors = {
            "Green.TButton": {"bg": "#00cc44", "hover": "#00dd55"},
            "Blue.TButton": {"bg": "#0088ff", "hover": "#2299ff"},
            "Orange.TButton": {"bg": "#ff8800", "hover": "#ff9922"},
            "Red.TButton": {"bg": "#cc0000", "hover": "#dd1111"},
            "Purple.TButton": {"bg": "#8800cc", "hover": "#9911dd"},
            "Pink.TButton": {"bg": "#ff1493", "hover": "#ff33aa"},
        }

        for name, c in colors.items():
            style.configure(name, font=("Segoe UI", 20, "bold"),
                          foreground="white", background=c["bg"])
            style.map(name, background=[("active", c["hover"])])

        style.configure("Dark.TFrame", background="#0a0a0a")
        style.configure("Card.TFrame", background="#1a1a1a", relief="ridge", borderwidth=2)
        style.configure("CardInner.TFrame", background="#1a1a1a")
        style.configure("Stats.TLabel", background="#1a1a1a", foreground="#00ff88")

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

    def _setup_ui(self):
        """
        Setup the user interface.
        
        BUG: Hardcoded padding may cause layout issues
        BUG: No scrollbar for stats if content overflows
        """
        main = ttk.Frame(self.root, style="Dark.TFrame")
        main.pack(fill="both", expand=True, padx=50, pady=35)  # BUG: Padding too large

        main.grid_rowconfigure(0, weight=1)
        main.grid_rowconfigure(1, weight=1)
        main.grid_rowconfigure(2, weight=5)
        main.grid_columnconfigure(0, weight=1)

        # Title
        title_frame = ttk.Frame(main, style="Dark.TFrame")
        title_frame.grid(row=0, column=0, sticky="nsew", pady=(0, 5))
        title_frame.grid_columnconfigure(0, weight=1)
        title_frame.grid_rowconfigure(0, weight=1)
        title_frame.grid_rowconfigure(1, weight=1)

        ttk.Label(title_frame, text="BITLIFE", font=("Segoe UI", 40, "bold"),
                  foreground="white", background="#0a0a0a").grid(row=0, column=0, sticky="s")
        ttk.Label(title_frame, text="Live your virtual life", font=("Segoe UI", 12, "italic"),
                  foreground="#666666", background="#0a0a0a").grid(row=1, column=0, sticky="n", pady=(0, 5))

        # Stats
        stats_frame = ttk.Frame(main, style="Dark.TFrame")
        stats_frame.grid(row=1, column=0, sticky="nsew", pady=(0, 10))
        stats_frame.grid_columnconfigure(0, weight=1)
        stats_frame.grid_rowconfigure(0, weight=1)

        card = ttk.Frame(stats_frame, style="Card.TFrame")
        card.grid(row=0, column=0, sticky="nsew", padx=10)
        card.grid_columnconfigure(0, weight=1)
        card.grid_rowconfigure(0, weight=1)

        inner = ttk.Frame(card, style="CardInner.TFrame")
        inner.grid(row=0, column=0, sticky="nsew", padx=25, pady=12)
        inner.grid_columnconfigure(0, weight=1)
        inner.grid_rowconfigure(0, weight=1)

        # BUG: Using Consolas font may not be available on all systems
        self.stats = ttk.Label(inner, style="Stats.TLabel", font=("Consolas", 20),
                              justify="left", anchor="w")
        self.stats.grid(row=0, column=0, sticky="w")

        # Buttons
        btns = ttk.Frame(main, style="Dark.TFrame")
        btns.grid(row=2, column=0, sticky="nsew", pady=(5, 0))
        btns.grid_columnconfigure(0, weight=1)
        btns.grid_rowconfigure(0, weight=1)

        btn_grid = ttk.Frame(btns, style="Dark.TFrame")
        btn_grid.grid(row=0, column=0, sticky="nsew", padx=20, pady=15)
        
        for i in range(4):
            btn_grid.grid_columnconfigure(i, weight=1, uniform="btncol")
        for i in range(2):
            btn_grid.grid_rowconfigure(i, weight=1, uniform="btnrow")

        menu = [
            ("Age Up", self.age_up, "Green.TButton"),
            ("Career", lambda: self.open("Career"), "Blue.TButton"),
            ("Relationships", self.open_relationships, "Pink.TButton"),
            ("Crime", self.open_crime, "Red.TButton"),
            ("Gamble", self.open_gamble, "Purple.TButton"),
            ("Save", self.save, "Green.TButton"),
            ("Load", self.load, "Blue.TButton"),
            ("New Game", self.new_game, "Orange.TButton"),
        ]

        for i, (text, cmd, style) in enumerate(menu):
            btn = ttk.Button(btn_grid, text=text, command=cmd, style=style)
            btn.grid(row=i//4, column=i%4, padx=20, pady=18, sticky="nsew")

    def open_window(self, win_class):
        """
        Open a child window.
        
        BUG: No validation that win_class exists
        BUG: No handling for window already being open
        """
        if not self.game.has_character():
            messagebox.showwarning("Error", "Create a character first!")
            return
        win_class(self.root, self.game, self.update_display)  # BUG: No error handling

    def open(self, name):
        """
        Open a specific window by name.
        
        BUG: Windows dictionary missing some entries
        """
        windows = {
            "Career": CareerWindow,
            # "Relationships": RelationshipWindow,
            # "Crime": CrimeWindow,
            "Gamble": GamblingWindow,
        }
        if name in windows:
            self.open_window(windows[name])
        # BUG: No else clause for invalid window names

    def open_relationships(self): self.open("Relationships")
    def open_crime(self): self.open("Crime")
    def open_gamble(self): self.open("Gamble")

    def update_display(self):
        """Update stats display."""
        self.stats.config(text=self.game.get_stats())  # BUG: No error handling

    def age_up(self):
        """
        Age up the character.
        
        BUG: No confirmation dialog before aging
        BUG: Death message may not display properly
        """
        if not self.game.has_character():
            messagebox.showwarning("Error", "Create a character first!")
            return
        result = self.game.age_up()
        self.update_display()
        # BUG: Death detection may not work correctly
        if "passed away" in str(result):
            messagebox.showinfo("Death", result)
        elif result and result != "Aged up successfully":
            messagebox.showinfo("Result", result)

    def save(self):
        """
        Save the game.
        
        BUG: No confirmation dialog before save
        """
        if not self.game.has_character():
            messagebox.showwarning("Error", "No character!")
            return
        if self.game.save():
            messagebox.showinfo("Saved", "Game saved!")
        else:
            messagebox.showinfo("Error", "Save failed!")

    def load(self):
        """
        Load the game.
        
        BUG: No confirmation dialog before load
        """
        if self.game.load():
            self.update_display()
            messagebox.showinfo("Loaded", "Game loaded!")
        else:
            messagebox.showerror("Error", "Load failed!")

#     def new_game(self):
#         """
#         Start a new game.
        
#         BUG: No confirmation dialog before new game
#         """
#         if messagebox.askyesno("New Game", "Start a new game?"):
#             from gui.character_creation_window import CharacterCreationWindow
#             CharacterCreationWindow(self.root, self.game, self.update_display)


# from gui.career_window import CareerWindow
# from gui.relationship_window import RelationshipWindow
# from gui.crime_window import CrimeWindow
# from gui.gambling_window import GamblingWindow