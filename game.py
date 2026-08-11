"""
Main Game class - coordinates all game systems and manages the game state.
"""

import json
import random
from logic.character_system import CharacterSystem
from logic.career_system import CareerSystem
# from logic.relationship_system import RelationshipSystem
# from logic.crime_system import CrimeSystem
from logic.gambling_system import GamblingSystem


class Game:
    """
    Main game controller managing character, state, and coordinating all systems.
    """
    
    def __init__(self):
        """Initialize the game with all subsystems"""
        self.character = None
        self.year = 2026
        
        # Initialize all game systems
        self.career = CareerSystem(self)
        # self.relationships = RelationshipSystem(self)
        # self.crime = CrimeSystem(self)
        self.gambling = GamblingSystem(self)
    
    def create_character(self, name, gender):
        """Create a new character and reset game state"""
        self.character = CharacterSystem(name, gender)
        self.year = 2026
    
    def has_character(self):
        """Check if character exists and is alive"""
        return self.character is not None and self.character.alive
    
    def get_character(self):
        """Get the current character"""
        return self.character
    
    def _death_check(self):
        """Calculate death probability based on age and health"""
        if not self.has_character():
            return False, ""
        
        char = self.character
        
        if char.age < 30:
            base = 0.001
        elif char.age < 50:
            base = 0.005
        elif char.age < 70:
            base = 0.02
        else:
            base = 0.09
        
        if char.health >= 80:
            health_mod = 0.5
        elif char.health >= 40:
            health_mod = 1.0
        else:
            health_mod = 2.0
        
        if random.random() < base * health_mod:
            causes = ["old age", "heart attack", "cancer", "accident"]
            if char.criminal_record:
                causes.append("jail")
            cause = random.choice(causes)
            char.alive = False
            return True, f"{char.name} passed away at age {char.age} from {cause}"
        return False, ""
    
    def age_up(self):
        """Progress the game by one year"""
        if not self.has_character():
            return "Create a character first!"
        
        char = self.character
        char.age += 1
        self.year += 1
        
        # Pay yearly salary if employed
        if char.job:
            salary_paid = self.career.pay_yearly_salary()
            char.job_experience += 1
        
        # Random stat changes
        char.change_stat('health', random.randint(-5, 5))
        char.change_stat('happiness', random.randint(-8, 12))
        char.change_stat('stress', random.randint(-5, 8))
        char.change_stat('social', random.randint(-5, 8))
        char.money = max(0, char.money + random.randint(-1000, 1500))
        
        # Relationship updates (Friends removed)
        if char.dating or char.married:
            char.relationship_years += 1
        
        # Death check
        dead, msg = self._death_check()
        if dead:
            return msg
        
        return "Aged up successfully"
    
    def save(self):
        """Save game state to JSON file"""
        if not self.has_character():
            return False
        try:
            data = {
                'character': self.character.to_dict(),
                'year': self.year
            }
            with open('bitlife_save.json', 'w') as f:
                json.dump(data, f)
            return True
        except:
            return False
    
    def load(self):
        """Load game state from JSON file"""
        try:
            with open('bitlife_save.json', 'r') as f:
                data = json.load(f)
            self.character = CharacterSystem.from_dict(data['character'])
            self.year = data.get('year', 2026)
            return True
        except:
            return False
    
    def get_stats(self):
        """Get formatted character statistics"""
        if not self.has_character():
            return "No character created"
        
        char = self.character
        status = "Alive" if char.alive else "Deceased"
        relationship = "Single"
        
        if char.married:
            relationship = f"Married to {char.spouse}"
        elif char.dating:
            relationship = f"Dating {char.spouse}"
        
        pet_list = "None"
        if char.pets:
            pet_parts = []
            for p in char.pets:
                pet_parts.append(f"{p['name']} ({p['type']})")
            pet_list = ", ".join(pet_parts)
        
        return f"""Name: {char.name} ({char.gender})  Year: {self.year}
Age: {char.age}  Money: ${char.money:,}
Health: {char.health}%  Happiness: {char.happiness}%
Smarts: {char.smarts}%  Stress: {char.stress}%
Job: {char.job or 'Unemployed'}  Experience: {char.job_experience//12} years
Relationship: {relationship}  Children: {len(char.children)}
Pets: {pet_list}
Status: {status}"""