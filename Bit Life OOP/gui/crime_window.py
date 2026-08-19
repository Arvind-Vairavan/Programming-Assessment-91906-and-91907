"""
So same with the crime system this will probably be the first and last version of this file,

with it looking pretty nice and functional, although it might not be the interactive thing in the game
I think it looks the best in terms of the menu window. I find like using the if else statement on one line makes my code more compact 
"""


from tkinter import ttk, messagebox
from gui.base_window import BaseWindow


class CrimeWindow(BaseWindow):
    def __init__(self, parent, game, on_update):
        super().__init__(parent, game, on_update, "Crime", 600, 700)
        self._setup()
    
    def _setup(self):
        self.add_title("CRIMINAL ACTIVITIES", "#ff2222")
        ttk.Label(self.win, text="Choose your crime carefully...", font=("Segoe UI", 11, "italic"), foreground="#888888", background="#0a0a0a").pack(pady=(0, 10))
        ttk.Separator(self.win, orient="horizontal").pack(fill="x", padx=20, pady=5)
        
        char = self.game.get_character()
        self._stats(char)
        ttk.Separator(self.win, orient="horizontal").pack(fill="x", padx=20, pady=10)
        
        crimes = self.game.crime.get_available_crimes()
        self.scrollable(crimes, lambda p, c: self._crime_card(p, c))
        self.add_close()
    
    def _stats(self, char):
        card = ttk.Frame(self.win, style="Card.TFrame")
        card.pack(fill="x", padx=20, pady=10)
        inner = ttk.Frame(card, style="CardInner.TFrame")
        inner.pack(fill="x", padx=15, pady=10)
        
        ttk.Label(inner, text=f"$ {char.money if char else 0:,}", font=("Segoe UI", 14, "bold"), foreground="#00ff44", background="#1a1a1a").pack(side="left", expand=True)
        record = self.game.crime.get_crime_record()
        ttk.Label(inner, text=f"RECORD: {'YES' if record else 'NO'}", font=("Segoe UI", 14, "bold"), foreground="#ff4444" if record else "#44ff44", background="#1a1a1a").pack(side="left", expand=True)
        ttk.Label(inner, text=f"CRIMES: {self.game.crime.get_crime_count()}", font=("Segoe UI", 14, "bold"), foreground="#ff8800", background="#1a1a1a").pack(side="left", expand=True)
    
    def _crime_card(self, parent, crime):
        self.card(parent, lambda i: self._card_content(i, crime))
    
    def _card_content(self, inner, crime):
        icons = {"Theft":"","Robbery":"","Grand Theft Auto":"","Bank Robbery":"","Cyber Crime":"","Arson":""}
        ttk.Label(inner, text=f"{icons.get(crime['name'], '')} {crime['name']}", font=("Segoe UI", 14, "bold"), foreground="white", background="#1a1a1a").pack(anchor="w")
        
        details = ttk.Frame(inner, style="CardInner.TFrame")
        details.pack(anchor="w", pady=(5, 0))
        ttk.Label(details, text=f"$ {crime['reward']:,}", font=("Segoe UI", 11), foreground="#ffd700", background="#1a1a1a").pack(side="left", padx=(0, 20))
        
        risk_color = "#44ff44" if crime["risk"] < 30 else "#ff8800" if crime["risk"] < 50 else "#ff2222"
        ttk.Label(details, text=f"{crime['risk']}%", font=("Segoe UI", 11), foreground=risk_color, background="#1a1a1a").pack(side="left")
        
        frame = ttk.Frame(inner, style="CardInner.TFrame")
        frame.pack(side="right", padx=(10, 0))
        ttk.Button(frame, text="COMMIT", command=lambda: self._commit(crime), style="Red.TButton").pack(anchor="center", pady=5)
    
    def _commit(self, crime):
        r = self.game.crime.commit_crime(crime)
        self.win.destroy()
        self.on_update()
        icon = "" if "successful" in r.lower() else "" if "jail" in r.lower() else ""
        messagebox.showinfo("Result", f"{icon} {r}")