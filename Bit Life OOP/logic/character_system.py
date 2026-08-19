"""
Character class representing the player's virtual life.
Contains all character attributes and basic stat management.
"""

import random


class CharacterSystem:
    """Main character class representing the player's virtual life"""
    
    def __init__(self, name, gender):
        """Initialize a new character with random starting stats"""
        # Identity
        self.name = name
        self.gender = gender
        
        # Core stats
        self.age = 18
        self.money = random.randint(1000, 5000)
        self.happiness = random.randint(50, 80)
        self.health = random.randint(50, 90)
        self.smarts = random.randint(40, 80)
        self.stress = random.randint(20, 50)
        self.social = random.randint(30, 70)
        
        # Career system
        self.job = None
        self.job_experience = 0
        self.last_promotion_age = 0
        
        # Relationship system (Friends removed)
        self.married = False
        self.spouse = None
        self.children = []
        self.dating = False
        self.relationship_years = 0
        self.last_relationship_event = 0
        
        # Pets
        self.pets = []
        
        # Crime system
        self.crimes = 0
        self.criminal_record = False
        
        # Status tracking
        self.alive = True

    def change_stat(self, stat, amount):
        """Safely change a numeric stat, keeping it within 0-100 range"""
        if hasattr(self, stat):
            current = getattr(self, stat)
            if isinstance(current, (int, float)):
                setattr(self, stat, max(0, min(100, current + amount)))

    def add_money(self, amount):
        """Add money to character, ensuring it never goes negative"""
        self.money = max(0, self.money + amount)

    def to_dict(self):
        """Convert character to dictionary for saving"""
        return {k: v for k, v in self.__dict__.items()}

    @classmethod
    def from_dict(cls, data):
        """Create character from saved dictionary data"""
        char = cls(data['name'], data['gender'])
        for key, value in data.items():
            if hasattr(char, key):
                setattr(char, key, value)
        return char