"""
Version 1 of gambling system

still has a lot of bug which I have pointed out and pretty basic code 
I decided not to have aclass for the horse racing game because I don't have enough time 
to make the horse racing game logic that good to be worthy of havings it s own class, so it is just a function in the gambling class
"""

import random
from typing import List, Tuple, Optional, Dict, Any


class SlotMachine:
    """
    Slot Machine with 7 symbols and payout multipliers.
    
    BUG: Jackpot calculation uses wrong multiplier
    BUG: Pair matching logic doesn't work correctly
    BUG: Win messages don't trigger properly
    """
    
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
        """
        Spin the slot machine.
        
        BUG: Doesn't check if bet is valid (could be negative)
        BUG: Happiness changes even if bet was invalid
        """
        char = self.game.character
        
        # BUG: No validation for negative bet amounts
        if char.money < bet:
            return {"error": "Not enough money!"}
        
        char.add_money(-bet)
        
        self.last_spin = [random.choice(self.SYMBOLS) for _ in range(3)]
        symbols = [s['symbol'] for s in self.last_spin]
        
        payout = self._calculate_payout(bet)
        
        if payout > 0:
            char.add_money(payout)
            # BUG: Happiness gain is too large for small wins
            char.change_stat('happiness', min(20, payout // 100))
            self.win_message = self._get_win_message(payout)
        else:
            # BUG: Losing always decreases happiness by 5, even for tiny bets
            char.change_stat('happiness', -5)
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
        """
        Calculate payout based on symbols.
        
        BUG: Jackpot should be 100x but uses wrong multiplier
        BUG: Pair matching doesn't handle all combinations
        """
        # BUG: Jackpot should be 100x, not 50x
        if all(s['symbol'] == '7️⃣' for s in self.last_spin):
            return bet * 50  # BUG: Should be 100
        
        # Three of a kind
        if self.last_spin[0]['symbol'] == self.last_spin[1]['symbol'] == self.last_spin[2]['symbol']:
            return bet * self.last_spin[0]['payout']
        
        # BUG: Pair matching logic is flawed - doesn't correctly identify pairs
        if (self.last_spin[0]['symbol'] == self.last_spin[1]['symbol'] or
            self.last_spin[1]['symbol'] == self.last_spin[2]['symbol'] or
            self.last_spin[0]['symbol'] == self.last_spin[2]['symbol']):
            
            # BUG: This logic may return wrong payout for pairs
            if self.last_spin[0]['symbol'] == self.last_spin[1]['symbol']:
                return bet * (self.last_spin[0]['payout'] // 2)
            elif self.last_spin[1]['symbol'] == self.last_spin[2]['symbol']:
                return bet * (self.last_spin[1]['payout'] // 2)
            else:
                # BUG: This case may not cover all pair scenarios
                return bet * (self.last_spin[0]['payout'] // 2)
        
        return 0
    
    def _get_win_message(self, payout: int) -> str:
        """
        Generate win message.
        
        BUG: Message thresholds don't match actual payout values
        """
        # BUG: Thresholds are too high - many wins get "Small win"
        if payout >= 10000:  # BUG: Should be 5000
            return f"💰 JACKPOT! You won ${payout:,}! Incredible! 💰"
        elif payout >= 5000:  # BUG: Should be 1000
            return f"🎉 HUGE WIN! You won ${payout:,}! Amazing! 🎉"
        elif payout >= 1000:  # BUG: Should be 500
            return f"🌟 Great win! You won ${payout:,}! 🌟"
        elif payout >= 500:  # BUG: Should be 100
            return f"✨ Nice win! You won ${payout:,}! ✨"
        else:
            return f"✓ Small win! You won ${payout:,}"


class GamblingSystem:
    """
    Main gambling system.
    
    BUG: Roulette doesn't handle invalid choices
    BUG: Horse racing doesn't validate horse name
    """
    
    def __init__(self, game_ref):
        self.game = game_ref
        self.slots = SlotMachine(game_ref)
    
    def slot_spin(self, bet: int) -> Dict[str, Any]:
        """Spin the slot machine"""
        return self.slots.spin(bet)
    
    def roulette_spin(self, bet: int, choice: str, number: int = None) -> Dict[str, Any]:
        """
        Spin roulette.
        
        BUG: No validation for choice parameter
        BUG: Number parameter not validated for range
        """
        char = self.game.character
        
        if char.money < bet:
            return {"error": "Not enough money!"}
        
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
        
        # BUG: No handling for invalid choice values
        if choice == "red" and result_color == "Red":
            win = True
            win_amount = bet * 2
        elif choice == "black" and result_color == "Black":
            win = True
            win_amount = bet * 2
        elif choice == "number" and number is not None and result == number:
            win = True
            win_amount = bet * 35
        # BUG: No else clause for invalid choices
        
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
        """
        Place a bet on a horse race.
        
        BUG: No validation for horse_name
        BUG: Duplicate horse names possible
        """
        char = self.game.character
        
        if char.money < bet:
            return {"error": "Not enough money!"}
        
        horses = [
            {"name": "Thunder", "odds": 3, "emoji": "⚡"},
            {"name": "Lightning", "odds": 5, "emoji": "🌩️"},
            {"name": "Shadow", "odds": 8, "emoji": "🌑"},
            {"name": "Storm", "odds": 2, "emoji": "🌪️"},
        ]
        
        char.add_money(-bet)
        
        winner = random.choice(horses)
        
        # BUG: Case sensitivity - "thunder" won't match "Thunder"
        if horse_name == winner["name"]:
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