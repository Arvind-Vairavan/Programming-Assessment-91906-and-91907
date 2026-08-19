"""
VERSION 2: FIXED CODE WITH IMPROVEMENTS
========================================
This version contains the fixed gambling system with all bugs addressed.
"""

import random
from typing import List, Tuple, Optional, Dict, Any


class SlotMachine:
    
    SYMBOLS = [
        {'symbol': '🍒', 'name': 'Cherry', 'payout': 2},
        {'symbol': '🍋', 'name': 'Lemon', 'payout': 3},
        {'symbol': '🍊', 'name': 'Orange', 'payout': 4},
        {'symbol': '🍇', 'name': 'Grape', 'payout': 5},
        {'symbol': '🔔', 'name': 'Bell', 'payout': 10},
        {'symbol': '💎', 'name': 'Diamond', 'payout': 20},
        {'symbol': '7️⃣', 'name': 'Seven', 'payout': 50},
    ]
    
    def __init__(self, game_ref):
        self.game = game_ref
        self.last_spin = []
        self.last_payout = 0
        self.win_message = ""
    
    def spin(self, bet: int) -> Dict[str, Any]:
        char = self.game.character
        
        if bet <= 0:
            return {"error": "Bet must be greater than 0!"}
        
        if char.money < bet:
            return {"error": "Not enough money!"}
        
        char.add_money(-bet)
        
        self.last_spin = [random.choice(self.SYMBOLS) for _ in range(3)]
        symbols = [s['symbol'] for s in self.last_spin]
        
        payout = self._calculate_payout(bet)
        
        if payout > 0:
            char.add_money(payout)
            happiness_gain = min(20, max(5, payout // 100))
            char.change_stat('happiness', happiness_gain)
            self.win_message = self._get_win_message(payout)
        else:
            happiness_loss = min(10, bet // 10)
            char.change_stat('happiness', -happiness_loss)
            self.win_message = "No match! Better luck next time!"
        
        self.last_payout = payout
        
        return {
            "symbols": symbols,
            "bet": bet,
            "payout": payout,
            "message": self.win_message,
            "money": char.money,
            "win": payout > 0
        }
    
    def _calculate_payout(self, bet: int) -> int:
        if all(s['symbol'] == '7️⃣' for s in self.last_spin):
            return bet * 100
        
        if self.last_spin[0]['symbol'] == self.last_spin[1]['symbol'] == self.last_spin[2]['symbol']:
            return bet * self.last_spin[0]['payout']
        
        symbol_counts = {}
        for s in self.last_spin:
            symbol_counts[s['symbol']] = symbol_counts.get(s['symbol'], 0) + 1
        
        for symbol, count in symbol_counts.items():
            if count == 2:
                for s in self.SYMBOLS:
                    if s['symbol'] == symbol:
                        return bet * (s['payout'] // 2)
        
        return 0
    
    def _get_win_message(self, payout: int) -> str:
        if payout >= 5000:
            return f"💰 JACKPOT! You won ${payout:,}! Incredible! 💰"
        elif payout >= 1000:
            return f"🎉 HUGE WIN! You won ${payout:,}! Amazing! 🎉"
        elif payout >= 500:
            return f"🌟 Great win! You won ${payout:,}! 🌟"
        elif payout >= 100:
            return f"✨ Nice win! You won ${payout:,}! ✨"
        else:
            return f"✓ Small win! You won ${payout:,}"


class GamblingSystem:
    
    def __init__(self, game_ref):
        self.game = game_ref
        self.slots = SlotMachine(game_ref)
    
    def slot_spin(self, bet: int) -> Dict[str, Any]:
        return self.slots.spin(bet)
    
    def roulette_spin(self, bet: int, choice: str, number: int = None) -> Dict[str, Any]:
        char = self.game.character
        
        if bet <= 0:
            return {"error": "Bet must be greater than 0!"}
        
        if char.money < bet:
            return {"error": "Not enough money!"}
        
        valid_choices = ["red", "black", "number"]
        if choice not in valid_choices:
            return {"error": f"Invalid choice! Must be one of: {', '.join(valid_choices)}"}
        
        if choice == "number":
            if number is None:
                return {"error": "Please select a number!"}
            if not isinstance(number, int) or number < 0 or number > 36:
                return {"error": "Number must be between 0 and 36!"}
        
        char.add_money(-bet)
        result = random.randint(0, 36)
        
        if result == 0:
            result_color = "Green"
        elif result % 2 == 0:
            result_color = "Black"
        else:
            result_color = "Red"
        
        win = False
        win_amount = 0
        message = ""
        
        if choice == "red" and result_color == "Red":
            win = True
            win_amount = bet * 2
        elif choice == "black" and result_color == "Black":
            win = True
            win_amount = bet * 2
        elif choice == "number" and number is not None and result == number:
            win = True
            win_amount = bet * 35
        
        if win:
            char.add_money(win_amount)
            char.change_stat('happiness', 10)
            message = f"🎯 Ball landed on {result} ({result_color})! You win ${win_amount:,}! 🎯"
        else:
            char.change_stat('happiness', -5)
            message = f"Ball landed on {result} ({result_color}). You lose."
        
        return {
            "result": result,
            "color": result_color,
            "bet": bet,
            "win": win,
            "win_amount": win_amount,
            "message": message,
            "money": char.money
        }
    
    def horse_race(self, bet: int, horse_name: str) -> Dict[str, Any]:
        char = self.game.character
        
        if bet <= 0:
            return {"error": "Bet must be greater than 0!"}
        
        if char.money < bet:
            return {"error": "Not enough money!"}
        
        horses = [
            {"name": "Thunder", "odds": 3, "emoji": "⚡"},
            {"name": "Lightning", "odds": 5, "emoji": "🌩️"},
            {"name": "Shadow", "odds": 8, "emoji": "🌑"},
            {"name": "Storm", "odds": 2, "emoji": "🌪️"},
        ]
        
        horse_names = [h["name"].lower() for h in horses]
        if horse_name.lower() not in horse_names:
            return {"error": f"Invalid horse! Choose from: {', '.join(h['name'] for h in horses)}"}
        
        char.add_money(-bet)
        
        winner = random.choice(horses)
        
        if horse_name.lower() == winner["name"].lower():
            win_amount = bet * winner["odds"]
            char.add_money(win_amount)
            char.change_stat('happiness', 20)
            message = f"🏇 {winner['emoji']} {winner['name']} wins! You win ${win_amount:,}! 🏇"
            win = True
        else:
            char.change_stat('happiness', -5)
            message = f"🏇 {winner['emoji']} {winner['name']} won. You lose."
            win = False
            win_amount = 0
        
        return {
            "winner": winner["name"],
            "winner_emoji": winner["emoji"],
            "bet": bet,
            "win": win,
            "win_amount": win_amount,
            "message": message,
            "money": char.money
        }