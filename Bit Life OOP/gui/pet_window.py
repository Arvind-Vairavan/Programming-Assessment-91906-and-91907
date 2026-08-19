"""
So this is the pet window
"""


from tkinter import ttk, messagebox
from gui.base_window import BaseWindow


class PetAdoptionWindow(BaseWindow):
    def __init__(self, parent, game, on_update):
        super().__init__(parent, game, on_update, "Pet Adoption", 500, 600)
        self._setup()
    
    def _setup(self):
        self.add_title("PET ADOPTION", "#00ff88")
        char = self.game.get_character()
        
        ttk.Label(self.win, text=f"$ {char.money if char else 0:,}", font=("Segoe UI", 12), foreground="#00ccff", background="#0a0a0a").pack(pady=5)
        ttk.Label(self.win, text=f"Current pets: {len(char.pets) if char else 0}", font=("Segoe UI", 12), foreground="#cccccc", background="#0a0a0a").pack(pady=(0, 5))
        ttk.Separator(self.win, orient="horizontal").pack(fill="x", padx=20, pady=10)
        
        pets = self.game.relationships.get_available_pets()
        self.scrollable(pets, lambda p, pet: self._pet_card(p, pet))
        self.add_close()
    
    def _pet_card(self, parent, pet):
        self.card(parent, lambda i: self._card_content(i, pet))
    
    def _card_content(self, inner, pet):
        emojis = {"Dog":"","Cat":"","Bird":"","Fish":"","Hamster":"","Rabbit":"","Turtle":""}
        ttk.Label(inner, text=f"{emojis.get(pet['name'], '')} {pet['name']}", font=("Segoe UI", 14, "bold"), foreground="white", background="#1a1a1a").pack(anchor="w")
        ttk.Label(inner, text=f"$ {pet['cost']:,}", font=("Segoe UI", 12), foreground="#ffd700", background="#1a1a1a").pack(anchor="w", pady=(3, 0))
        frame = ttk.Frame(inner, style="CardInner.TFrame")
        frame.pack(side="right", padx=(10, 0))
        ttk.Button(frame, text="ADOPT", command=lambda: self._adopt(pet), style="Green.TButton").pack(anchor="center", pady=5)
    
    def _adopt(self, pet):
        r = self.game.relationships.adopt_pet(pet)
        self.win.destroy()
        self.on_update()
        messagebox.showinfo("Adoption", r)


class PetManagementWindow(BaseWindow):
    def __init__(self, parent, game, on_update):
        char = game.get_character()
        if not char or not char.pets:
            messagebox.showinfo("Pets", "You don't have any pets!")
            return
        super().__init__(parent, game, on_update, "Your Pets", 500, 500)
        self._setup()
    
    def _setup(self):
        self.add_title("YOUR PETS", "#ffd700")
        char = self.game.get_character()
        self.scrollable(char.pets, lambda p, pet: self._pet_card(p, pet))
        self.add_close()
    
    def _pet_card(self, parent, pet):
        self.card(parent, lambda i: self._card_content(i, pet))
    
    def _card_content(self, inner, pet):
        emojis = {"Dog":"","Cat":"","Bird":"","Fish":"","Hamster":"","Rabbit":"","Turtle":""}
        ttk.Label(inner, text=f"{emojis.get(pet['type'], '')} {pet['name']}", font=("Segoe UI", 14, "bold"), foreground="white", background="#1a1a1a").pack(anchor="w")
        ttk.Label(inner, text=f"Type: {pet['type']}", font=("Segoe UI", 11), foreground="#888888", background="#1a1a1a").pack(anchor="w", pady=(3, 0))
        
        frame = ttk.Frame(inner, style="CardInner.TFrame")
        frame.pack(side="right", padx=(10, 0))
        ttk.Button(frame, text="Rename", command=lambda: self._rename(pet), style="Blue.TButton").pack(pady=3)
        ttk.Button(frame, text="Give Away", command=lambda: self._give(pet), style="Red.TButton").pack(pady=3)
    
    def _rename(self, pet):
        win = BaseWindow(self.win, self.game, None, "Rename Pet", 350, 200)
        ttk.Label(win.win, text=f"Rename {pet['name']}:", font=("Segoe UI", 12), foreground="white", background="#0a0a0a").pack(pady=10)
        entry = ttk.Entry(win.win, font=("Segoe UI", 12), width=25)
        entry.pack(pady=5, padx=30)
        entry.insert(0, pet['name'])
        entry.focus()
        
        def do_rename():
            new = entry.get().strip()
            if new and self.game.relationships.rename_pet(pet['name'], new):
                win.win.destroy()
                self.win.destroy()
                self.on_update()
                messagebox.showinfo("Success", f"Renamed to {new}!")
        ttk.Button(win.win, text="Rename", command=do_rename, style="Green.TButton").pack(pady=10)
        ttk.Button(win.win, text="Cancel", command=win.win.destroy, style="Red.TButton").pack()
    
    def _give(self, pet):
        if messagebox.askyesno("Give Away", f"Give away {pet['name']}?"):
            if self.game.relationships.give_away_pet(pet['name']):
                self.win.destroy()
                self.on_update()
                messagebox.showinfo("Success", "Pet given away!")