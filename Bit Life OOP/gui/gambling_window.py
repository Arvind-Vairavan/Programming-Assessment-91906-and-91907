from tkinter import ttk
from gui.base_window import BaseWindow
from gui.gui_helpers import button


class GamblingWindow(BaseWindow):
    def __init__(self, parent, game, on_update):
        super().__init__(parent, game, on_update, "Gambling", 500, 600)
        self.win.configure(bg="black")
        self._setup()
        self._update_money()
    
    def _setup(self):
        self.add_title("🎰 CASINO 🎰", "#ffd700")
        
        # Money display - will be updated live
        self.money_label = ttk.Label(
            self.win, 
            font=("Segoe UI", 16, "bold"), 
            foreground="#00ff88", 
            background="black"
        )
        self.money_label.pack(pady=10)
        
        # Games - Craps removed
        games = [
            ("🎰 Slots", self._slots, "Orange.TButton"),
            ("🎲 Roulette", self._roulette, "Red.TButton"),
            ("🏇 Horse Racing", self._horses, "Purple.TButton"),
        ]
        
        for text, cmd, style in games:
            button(self.win, text, cmd, style)
        self.add_close()
    
    def _update_money(self):
        """Update the money display to match character's actual money"""
        char = self.game.get_character()
        if char:
            self.money_label.config(text=f"💰 ${char.money:,}")
        else:
            self.money_label.config(text="💰 $0")
    
    def _refresh_and_open(self, window_class):
        """Refresh money then open the subwindow"""
        self._update_money()
        window_class(self.win, self.game, lambda: self._on_subwindow_update())
    
    def _on_subwindow_update(self):
        """Called when a subwindow updates - refreshes money and main game"""
        self._update_money()
        if self.on_update:
            self.on_update()
    
    def _slots(self): 
        from gui.gambling_subwindows import SlotsWindow
        self._refresh_and_open(SlotsWindow)
    
    def _roulette(self): 
        from gui.gambling_subwindows import RouletteWindow
        self._refresh_and_open(RouletteWindow)
    
    def _horses(self): 
        from gui.gambling_subwindows import HorseRacingWindow
        self._refresh_and_open(HorseRacingWindow)
    
    def refresh(self):
        """Public method to refresh money display"""
        self._update_money()