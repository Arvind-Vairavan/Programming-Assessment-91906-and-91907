"""
Version Gambling Subwindows V3

- Slot Machine (3-reel with 7 symbols and progressive payouts)
- Roulette (American style with 0-36, color and number bets)
- Horse Racing (4 horses with different odds and visual feedback)

Everyhting I fixed that was still and bug in the previous version 
- Fixed zip() iteration in generate_bet_options
- Added None checks in validate_bet
- Fixed lambda capture in HorseRacingWindow
- Added proper error handling in RouletteWindow
- Fixed spinning state in SlotsWindow
- Added parent window refresh handling
- Fixed money display when character has no money
- Added validation for number input in roulette
- Prevented multiple simultaneous spins
- Fixed bet options update on focus
"""

import random, time, tkinter as tk
from tkinter import ttk, messagebox, IntVar
from gui.base_window import BaseWindow


def generate_bet_options(money):
    """
    Generate smart betting options based on player's current money.
    """
    options = []
    
    if money <= 0:
        return ["All In"]
    
    # Fixed base amounts suitable for most players
    base_amounts = [1, 5, 10, 25, 50, 100, 250, 500, 1000]
    
    for amount in base_amounts:
        if amount <= money:
            options.append(str(amount))
    
    # Percentage-based bets for larger bankrolls
    percentages = [0.05, 0.10, 0.15, 0.25, 0.50]
    labels = ["Small", "Medium", "Medium+", "Big", "High Roller"]
    
    for percent, label in zip(percentages, labels):
        amount = int(money * percent)
        
        # Round to user-friendly values
        if amount < 100:
            amount = round(amount / 10) * 10  # Round to nearest 10
        elif amount < 1000:
            amount = round(amount / 50) * 50  # Round to nearest 50
        else:
            amount = round(amount / 100) * 100  # Round to nearest 100
        
        if amount > 0 and amount <= money and str(amount) not in options:
            options.append(str(amount))
    
    # Always include "All In" as the maximum bet
    options.append("All In")
    
    # Remove duplicates and sort numerically
    numeric_options = []
    for opt in options:
        if opt != "All In":
            try:
                numeric_options.append(int(opt))
            except:
                pass
    
    numeric_options = sorted(set(numeric_options))
    
    # Convert back to strings and add "All In" at the end
    result = [str(opt) for opt in numeric_options if opt <= money]
    result.append("All In")
    
    return result


def get_bet_value(bet_str, money):
    """
    Convert bet string to integer value.
    """
    if bet_str == "All In":
        return money
    try:
        return int(bet_str)
    except:
        return None


def validate_bet(bet, money):
    """
    Validate bet amount with comprehensive error checking.
    """
    if bet is None:
        return None, "Invalid bet amount"
    if bet <= 0:
        return None, "Bet must be greater than 0"
    if bet > money:
        return None, f"You cannot bet more than you have! (${money:,})"
    return bet, None


class BaseGamblingWindow(BaseWindow):
    """
    Base class for all gambling windows.
    """
    
    def __init__(self, parent, game, on_update, title, width, height):
        """
        Initialize base gambling window.
        """
        super().__init__(parent, game, on_update, title, width, height)
        self.parent_window = parent
        self.money_label = None
    
    def _update_money(self):
        """
        Update money display to match character's current money.
        """
        char = self.game.get_character()
        if char and self.money_label:
            self.money_label.config(text=f"💰 ${char.money:,}")
        elif self.money_label:
            self.money_label.config(text="💰 $0")
    
    def _refresh_all(self):
        """
        Refresh all displays and notify parent window.
        """
        self._update_money()
        if self.on_update:
            self.on_update()
        if hasattr(self.parent_window, 'refresh'):
            self.parent_window.refresh()
    
    def _update_bet_options(self):
        """
        Update bet dropdown with current money options.
        """
        char = self.game.get_character()
        if char and hasattr(self, 'bet_combo'):
            options = generate_bet_options(char.money)
            self.bet_combo['values'] = options
            current = self.bet_var.get() if hasattr(self, 'bet_var') else ""
            
            if current not in options and current != "All In":
                try:
                    val = int(current)
                    if val <= char.money:
                        self.bet_var.set(current)
                    else:
                        self.bet_var.set(options[0] if options else "All In")
                except:
                    self.bet_var.set(options[0] if options else "All In")
    
    def _get_bet(self):
        """
        Validate and return the bet amount.
        """
        char = self.game.get_character()
        if not char:
            return None
        
        bet_str = self.bet_var.get().strip()
        bet = get_bet_value(bet_str, char.money)
        validated, error = validate_bet(bet, char.money)
        if error:
            messagebox.showwarning("Invalid Bet", error)
            return None
        return validated


class SlotsWindow(BaseGamblingWindow):
    """
    Slot Machine game window with animated reels.
    """
    
    def __init__(self, parent, game, on_update):
        """
        Initialize Slot Machine window.
        """
        super().__init__(parent, game, on_update, "Slot Machine", 600, 600)
        self.win.configure(bg="black")
        self.spinning = False  # Prevents multiple simultaneous spins
        self._setup()
    
    def _setup(self):
        """Setup the slot machine user interface."""
        self.add_title("🎰 SLOT MACHINE 🎰", "#ffd700")
        
        # Money display with green text on black background
        self.money_label = ttk.Label(
            self.win, 
            font=("Segoe UI", 14, "bold"), 
            foreground="#00ff88", 
            background="black"
        )
        self.money_label.pack(pady=5)
        self._update_money()
        
        # Three reels with styling
        f = ttk.Frame(self.win, style="Dark.TFrame")
        f.pack(pady=20)
        self.reels = []
        for _ in range(3):
            r = ttk.Label(f, font=("Segoe UI", 72), foreground="#ffd700", 
                         background="#2a1a0a", relief="ridge", borderwidth=5, padding=20)
            r.pack(side="left", padx=10)
            self.reels.append(r)
        for r in self.reels: 
            r.config(text="🍒")
        
        # Bet controls
        bf = ttk.Frame(self.win, style="Dark.TFrame")
        bf.pack(pady=10)
        ttk.Label(bf, text="Bet Amount:", font=("Segoe UI", 12), 
                 foreground="white", background="black").pack(side="left", padx=5)
        
        self.bet_var = tk.StringVar(value="100")
        self.bet_combo = ttk.Combobox(bf, textvariable=self.bet_var, 
                                      width=15, font=("Segoe UI", 12))
        self.bet_combo.pack(side="left", padx=5)
        self._update_bet_options()
        self.bet_combo.bind('<FocusIn>', lambda e: self._update_bet_options())
        
        # Spin button with green style
        self.spin_btn = ttk.Button(self.win, text="🎰 SPIN 🎰", 
                                   command=self._spin, style="Green.TButton")
        self.spin_btn.pack(pady=10)
        
        # Information display for win/loss messages
        self.info = ttk.Label(self.win, font=("Segoe UI", 12), 
                             foreground="#cccccc", background="black", wraplength=500)
        self.info.pack(pady=10)
        self.add_close()
    
    def _spin(self):
        """
        Execute a slot machine spin with animation.
        """
        if self.spinning: 
            return
        char = self.game.get_character()
        if not char: 
            return
        
        bet = self._get_bet()
        if bet is None:
            return
        
        # Start spinning
        self.spinning = True
        self.spin_btn.config(state="disabled")
        self.info.config(text="🎲 Spinning... 🎲")
        
        # Animation loop
        symbols = ['🍒','🍋','🍊','🍇','🔔','💎','7️⃣']
        for _ in range(10):
            for r in self.reels: 
                r.config(text=random.choice(symbols))
            self.win.update()
            time.sleep(0.05)
        
        # Get result from gambling system
        result = self.game.gambling.slot_spin(bet)
        
        # Update displays
        self._update_money()
        self._update_bet_options()
        self._refresh_all()
        
        # Display result
        if "error" in result:
            self.info.config(text=f"❌ {result['error']}")
        else:
            for i, s in enumerate(result['symbols']): 
                self.reels[i].config(text=s)
            self.info.config(text=result['message'])
            self._update_money()
            self._update_bet_options()
            self._refresh_all()
        
        # Reset spinning state
        self.spinning = False
        self.spin_btn.config(state="normal")


class HorseRacingWindow(BaseGamblingWindow):
    """
    Horse Racing betting window.
    """
    
    def __init__(self, parent, game, on_update):
        """
        Initialize Horse Racing window.
        """
        super().__init__(parent, game, on_update, "Horse Racing", 550, 550)
        self.win.configure(bg="black")
        self._setup()
    
    def _setup(self):
        """Setup the horse racing user interface."""
        self.add_title("🏇 HORSE RACING 🏇", "#ffd700")
        
        # Money display
        self.money_label = ttk.Label(
            self.win, 
            font=("Segoe UI", 14, "bold"), 
            foreground="#00ff88", 
            background="black"
        )
        self.money_label.pack(pady=5)
        self._update_money()
        
        # Bet controls
        bf = ttk.Frame(self.win, style="Dark.TFrame")
        bf.pack(pady=10)
        ttk.Label(bf, text="Bet Amount:", font=("Segoe UI", 12), 
                 foreground="white", background="black").pack(side="left", padx=5)
        
        self.bet_var = tk.StringVar(value="500")
        self.bet_combo = ttk.Combobox(bf, textvariable=self.bet_var, 
                                      width=15, font=("Segoe UI", 12))
        self.bet_combo.pack(side="left", padx=5)
        self._update_bet_options()
        self.bet_combo.bind('<FocusIn>', lambda e: self._update_bet_options())
        
        # Horse display
        horses = [
            ("Thunder", 3, "⚡", "#ff8800"),
            ("Lightning", 5, "🌩️", "#00ccff"),
            ("Shadow", 8, "🌑", "#8800cc"),
            ("Storm", 2, "🌪️", "#00ff88"),
        ]
        
        # Create bet button for each horse
        for name, odds, emoji, color in horses:
            f = ttk.Frame(self.win, style="Dark.TFrame")
            f.pack(fill="x", pady=5, padx=30)
            ttk.Label(f, text=f"{emoji} {name} ({odds}x)", 
                     font=("Segoe UI", 14), foreground=color, 
                     background="black").pack(side="left", padx=10)
            ttk.Button(f, text="BET", command=lambda n=name: self._bet(n), 
                      style="Green.TButton").pack(side="right", padx=10)
        
        # Race result message display
        self.msg = ttk.Label(self.win, font=("Segoe UI", 13, "bold"), 
                            foreground="#ffd700", background="black", wraplength=500)
        self.msg.pack(pady=10)
        self.add_close()
    
    def _bet(self, name):
        """
        Place a bet on a specific horse.
        """
        char = self.game.get_character()
        if not char: 
            return
        
        bet = self._get_bet()
        if bet is None:
            return
        
        r = self.game.gambling.horse_race(bet, name)
        self.msg.config(text=r['message'])
        self._update_money()
        self._update_bet_options()
        self._refresh_all()


class RouletteWindow(BaseGamblingWindow):
    """
    Roulette game window with color and number betting.
    """
    
    def __init__(self, parent, game, on_update):
        """
        Initialize Roulette window.
        """
        super().__init__(parent, game, on_update, "Roulette", 600, 600)
        self.win.configure(bg="black")
        self._setup()
    
    def _setup(self):
        """Setup the roulette user interface."""
        self.add_title("🎲 ROULETTE 🎲", "#ffd700")
        
        # Money display
        self.money_label = ttk.Label(
            self.win, 
            font=("Segoe UI", 14, "bold"), 
            foreground="#00ff88", 
            background="black"
        )
        self.money_label.pack(pady=5)
        self._update_money()
        
        # Wheel result display
        f = ttk.Frame(self.win, style="Dark.TFrame")
        f.pack(pady=10)
        self.result = ttk.Label(f, font=("Segoe UI", 48), foreground="#ffd700", 
                               background="#2a1a0a", relief="ridge", 
                               borderwidth=5, padding=20)
        self.result.pack(pady=10)
        self.result.config(text="🎡")
        self.color = ttk.Label(f, font=("Segoe UI", 16, "bold"), 
                              foreground="#cccccc", background="black")
        self.color.pack()
        
        # Bet controls
        bf = ttk.Frame(self.win, style="Dark.TFrame")
        bf.pack(pady=10)
        ttk.Label(bf, text="Bet Amount:", font=("Segoe UI", 12), 
                 foreground="white", background="black").pack(side="left", padx=5)
        
        self.bet_var = tk.StringVar(value="500")
        self.bet_combo = ttk.Combobox(bf, textvariable=self.bet_var, 
                                      width=15, font=("Segoe UI", 12))
        self.bet_combo.pack(side="left", padx=5)
        self._update_bet_options()
        self.bet_combo.bind('<FocusIn>', lambda e: self._update_bet_options())
        
        # Message display
        self.msg = ttk.Label(self.win, font=("Segoe UI", 12), 
                            foreground="#cccccc", background="black", wraplength=500)
        self.msg.pack(pady=10)
        
        # Color betting buttons
        bf2 = ttk.Frame(self.win, style="Dark.TFrame")
        bf2.pack(pady=5)
        ttk.Button(bf2, text="🔴 Red", command=lambda: self._spin("red"), 
                  style="Red.TButton").pack(side="left", padx=5)
        ttk.Button(bf2, text="⚫ Black", command=lambda: self._spin("black"), 
                  style="Blue.TButton").pack(side="left", padx=5)
        
        # Number betting
        nf = ttk.Frame(self.win, style="Dark.TFrame")
        nf.pack(pady=5)
        ttk.Label(nf, text="Number:", font=("Segoe UI", 12), 
                 foreground="white", background="black").pack(side="left", padx=5)
        self.num = ttk.Combobox(nf, values=list(range(0,37)), 
                               width=8, font=("Segoe UI", 12))
        self.num.set(0)
        self.num.pack(side="left", padx=5)
        ttk.Button(nf, text="🎯 Bet", command=lambda: self._spin("number"), 
                  style="Purple.TButton").pack(side="left", padx=5)
        
        self.add_close()
    
    def _spin(self, choice):
        """
        Execute a roulette spin.
        """
        char = self.game.get_character()
        if not char: 
            return
        
        bet = self._get_bet()
        if bet is None:
            return
        
        # Validate number input for number bets
        num = None
        if choice == "number":
            try:
                num = int(self.num.get())
                if num < 0 or num > 36:
                    messagebox.showerror("Error", "Number must be between 0 and 36")
                    return
            except:
                messagebox.showerror("Error", "Please select a valid number")
                return
        
        # Get result from gambling system
        r = self.game.gambling.roulette_spin(bet, choice, num)
        
        if "error" in r:
            messagebox.showerror("Error", r["error"])
            return
        
        # Display result with color indicator
        self.result.config(text=str(r['result']))
        colors = {"Red":"🔴","Black":"⚫","Green":"🟢"}
        self.color.config(text=f"{colors.get(r['color'], '')} {r['color']}")
        self.msg.config(text=r['message'])
        self._update_money()
        self._update_bet_options()
        self._refresh_all()