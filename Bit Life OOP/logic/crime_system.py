"""
Crime system managing criminal activities and consequences.

This code is fairly simple it is about the crime button on my man screen it does not do too much 
other than  look good and display messages of the outcome after you have commited the crime
this is the first version and I probably wont be doing a second version.
"""

import random
from data.constants import CRIMES


class CrimeSystem:
    def __init__(self, game):
        """
        Initialize the crime system.
        """
        self.game = game
    
    def _get_character(self):
        """Helper to get current character, with validation"""
        return self.game.character if self.game.has_character() else None
    
    def commit_crime(self, crime):
        """
        Attempt to commit a crime.
        """
        char = self._get_character()
        if not char:
            return "No character found!"
        
        if random.random() < 1 - (crime["risk"] / 100):
            char.add_money(crime["reward"])
            char.crimes += 1
            if char.crimes >= 3:
                char.criminal_record = True
            return f"Crime successful! Made ${crime['reward']}"
        else:
            if random.random() < 0.5:
                char.criminal_record = True
                return "Got caught! Went to jail!"
            return "Crime failed! Escaped!"
    
    def get_available_crimes(self):
        """Get list of all available crimes"""
        return CRIMES
    
    def get_crime_record(self):
        """Get criminal record status"""
        char = self._get_character()
        if not char:
            return False
        return char.criminal_record
    
    def get_crime_count(self):
        """Get number of crimes committed"""
        char = self._get_character()
        return char.crimes if char else 0
