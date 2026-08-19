"""

"""


from tkinter import ttk, messagebox
from gui.base_window import BaseWindow
from gui.gui_helpers import button


class RelationshipWindow(BaseWindow):
    def __init__(self, parent, game, on_update):
        super().__init__(parent, game, on_update, "Relationship Management", 550, 500)
        self._setup()
    
    def _setup(self):
        self.add_title("RELATIONSHIP MANAGEMENT", "#ff69b4")
        char = self.game.get_character()
        
        status = self.game.relationships.get_relationship_status()
        btns = self._love_buttons()
        self._section("Love Life", status, btns)
        
        pets = self.game.relationships.get_pets()
        text = "Pets: " + ", ".join([f"{p['name']} ({p['type']})" for p in pets]) if pets else "No pets"
        btns = [
            {"text": "Adopt Pet", "action": self._open_pets, "style": "Green.TButton"},
            {"text": "Manage Pets", "action": self._open_pet_mgmt, "style": "Orange.TButton"},
        ]
        self._section("Pets", text, btns)
        self.add_close()
    
    def _section(self, title, content, btns=None):
        card = ttk.Frame(self.win, style="Card.TFrame")
        card.pack(fill="x", padx=20, pady=8)
        inner = ttk.Frame(card, style="CardInner.TFrame")
        inner.pack(fill="x", padx=15, pady=12)
        
        ttk.Label(inner, text=title, font=("Segoe UI", 13, "bold"), foreground="#00ccff", background="#1a1a1a").pack(anchor="w", pady=(0, 5))
        if content: ttk.Label(inner, text=content, font=("Segoe UI", 11), foreground="#cccccc", background="#1a1a1a", justify="left").pack(anchor="w", pady=(0, 5))
        if btns:
            f = ttk.Frame(inner, style="CardInner.TFrame")
            f.pack(fill="x", pady=(5, 0))
            for b in btns:
                button(f, b["text"], b["action"], b.get("style", "Blue.TButton"), side="left", padx=3, fill="x", expand=True)
    
    def _love_buttons(self):
        char = self.game.get_character()
        btns = []
        if not char.married and not char.dating: btns.append({"text": "Date Someone", "action": self._date, "style": "Purple.TButton"})
        if char.dating and not char.married: btns.append({"text": "Propose", "action": self._marry, "style": "Green.TButton"})
        if char.married: btns.append({"text": "Have Child", "action": self._child, "style": "Green.TButton"})
        if char.dating or char.married: btns.append({"text": "Break Up", "action": self._break, "style": "Red.TButton"})
        return btns
    
    def _exec(self, func):
        r = func()
        self.win.destroy()
        self.on_update()
        if r and isinstance(r, str): messagebox.showinfo("Result", r)
    
    def _date(self): self._exec(self.game.relationships.date_manual)
    def _marry(self):
        r = self.game.relationships.get_married()
        self.win.destroy()
        self.on_update()
        messagebox.showinfo("Result", r)
    def _break(self):
        char = self.game.get_character()
        if char and (char.dating or char.married):
            name = char.spouse
            if messagebox.askyesno("Break Up", f"Break up with {name}?"):
                r = self.game.relationships.break_up()
                self.win.destroy()
                self.on_update()
                messagebox.showinfo("Result", r)
    def _child(self): self._exec(self.game.relationships.have_child_manual)
    
    def _open_pets(self):
        from gui.pet_window import PetAdoptionWindow
        PetAdoptionWindow(self.win, self.game, self.on_update)
    
    def _open_pet_mgmt(self):
        from gui.pet_window import PetManagementWindow
        PetManagementWindow(self.win, self.game, self.on_update)