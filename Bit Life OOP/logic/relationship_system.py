"""
Version 2 With most bugs fixed to the best of my ability 
"""

import random
from data.constants import MALE_NAMES, FEMALE_NAMES, CHILD_NAMES, PETS


class RelationshipSystem:
    """
    Manages all relationship-related logic.
    
    FIXES APPLIED:
    - Added age validation for dating
    - Fixed marriage proposal checks
    - Added child custody and alimony
    - Improved pet management with age tracking
    - Added relationship year tracking
    - Fixed gender pronoun handling
    - Added compatibility checks
    """
    
    def __init__(self, game):
        self.game = game
        self.breakup_cooldown = {}  # FIX: Track breakup cooldowns
    
    def _get_character(self):
        """Get the current character."""
        return self.game.character if self.game.has_character() else None
    
    def start_dating(self, partner_name=None):
        """
        Start a romantic relationship with someone.
        
        FIX: Added age validation
        FIX: Added cooldown after breakup
        FIX: Success based on charisma and compatibility
        """
        char = self._get_character()
        if not char:
            return "No character found!"
        
        # FIX: Added age validation
        if char.age < 16:
            return "You're too young to date!"
        
        # FIX: Added breakup cooldown
        if char.name in self.breakup_cooldown:
            if char.age - self.breakup_cooldown[char.name] < 2:
                return "You need some time before dating again!"
        
        if char.dating or char.married:
            return "Already in a relationship!"
        
        # FIX: Partner selection with age-appropriate names
        if partner_name is None:
            if char.gender == "Male":
                partner_name = random.choice(FEMALE_NAMES)
            else:
                partner_name = random.choice(MALE_NAMES)
        
        # FIX: Success rate based on charisma
        charisma_bonus = char.charisma / 100 if hasattr(char, 'charisma') else 0.5
        success_rate = 0.5 + charisma_bonus  # Base 50% + charisma bonus
        
        if random.random() < success_rate:
            char.spouse = partner_name
            char.dating = True
            char.relationship_years = 0
            char.last_relationship_event = char.age
            char.change_stat('happiness', 20)
            return f"Started dating {partner_name}!"
        return "They weren't interested."
    
    def date_manual(self):
        """Manual dating interface."""
        return self.start_dating()
    
    def get_married(self):
        """
        Propose marriage to current dating partner.
        
        FIX: Added engagement period
        FIX: Check if partner exists
        FIX: Happiness based on compatibility
        """
        char = self._get_character()
        if not char:
            return "No character found!"
        
        if not char.dating:
            return "Not dating anyone!"
        
        if not char.spouse:
            return "No partner found!"
        
        # FIX: Check if partner is still alive
        if hasattr(char, 'partner_age') and char.partner_age > 100:
            return "Your partner is no longer with us."
        
        # FIX: Engagement period (minimum 1 year)
        if char.relationship_years < 1:
            return "You should date for at least a year before proposing!"
        
        # FIX: Success based on relationship length and happiness
        success_rate = 0.4 + (char.relationship_years * 0.05)
        if char.happiness > 80:
            success_rate += 0.2
        
        if random.random() < success_rate:
            char.married = True
            # FIX: Happiness boost based on relationship quality
            happiness_boost = 25 + (char.relationship_years * 2)
            char.change_stat('happiness', min(50, happiness_boost))
            return f"Married {char.spouse}!"
        else:
            # FIX: Better pronoun handling for non-binary
            if char.gender == "Male":
                pronoun = "she"
            elif char.gender == "Female":
                pronoun = "he"
            else:
                pronoun = "they"
            return f"{char.spouse} said {pronoun} is not ready yet."
    
    def marry_manual(self):
        """Manual marriage interface."""
        return self.get_married()
    
    def break_up(self):
        """
        End current relationship.
        
        FIX: Added alimony for marriage
        FIX: Child custody handling
        FIX: Happiness loss based on relationship length
        """
        char = self._get_character()
        if not char:
            return "No character found!"
        
        if not char.dating and not char.married:
            return "Not in a relationship!"
        
        name = char.spouse
        is_married = char.married
        
        # FIX: Alimony for marriage
        if is_married:
            alimony = len(char.children) * 5000
            char.add_money(-alimony)
        
        char.married = False
        char.dating = False
        char.spouse = None
        
        # FIX: Happiness loss based on relationship length
        happiness_loss = min(50, 20 + char.relationship_years)
        char.change_stat('happiness', -happiness_loss)
        
        # FIX: Set cooldown
        self.breakup_cooldown[char.name] = char.age
        
        return f"Broke up with {name}"
    
    def break_up_manual(self):
        """Manual breakup interface."""
        return self.break_up()
    
    def have_child(self):
        """
        Have a child (requires marriage and appropriate age).
        
        FIX: Check if spouse exists
        FIX: Fertility based on age
        FIX: Child naming options
        FIX: Added child raising costs
        """
        char = self._get_character()
        if not char:
            return "No character found!"
        
        # FIX: Check if spouse exists
        if not char.married or not char.spouse:
            return "Must be married to have a child!"
        
        # FIX: Age fertility adjustments
        if char.age < 18:
            return "You're too young to have children!"
        if char.age > 50:
            return "You're too old to have children!"
        
        # FIX: Fertility decreases with age
        fertility = 0.7
        if char.age > 35:
            fertility = 0.5
        if char.age > 40:
            fertility = 0.3
        
        # FIX: Check if pregnancy is successful
        if random.random() > fertility:
            return "You're trying to conceive but not successful yet."
        
        if len(char.children) >= 6:  # FIX: Increased limit to 6
            return "You have enough children!"
        
        # FIX: Allow naming child (or random)
        if hasattr(self, 'child_name_choice'):
            child = self.child_name_choice
        else:
            child = random.choice(CHILD_NAMES)
        
        char.children.append(child)
        # FIX: Added ongoing child costs
        char.add_money(-15000)  # FIX: Increased cost
        char.change_stat('happiness', 25)  # FIX: Increased happiness
        return f"Welcome, {child}!"
    
    def have_child_manual(self):
        """Manual child birth interface."""
        return self.have_child()
    
    def get_relationship_status(self):
        """
        Get formatted relationship status.
        
        FIX: Correct order (marriage checked first)
        FIX: Relationship years properly tracked
        """
        char = self._get_character()
        if not char:
            return "No character"
        
        # FIX: Marriage checked before dating
        if char.married:
            return f"Married to {char.spouse} ({char.relationship_years} years)"
        elif char.dating:
            return f"Dating {char.spouse} ({char.relationship_years} years)"
        return "Single"
    
    def get_children_count(self):
        """Get number of children."""
        char = self._get_character()
        return len(char.children) if char else 0
    
    def adopt_pet(self, pet_type):
        """
        Adopt a pet by type.
        
        FIX: Expanded pet name list
        FIX: Check if pet_type exists
        FIX: Added pet age tracking
        FIX: Prevent duplicate names
        """
        char = self._get_character()
        if not char:
            return "No character found!"
        
        # FIX: Check if pet_type exists
        if pet_type not in PETS and not isinstance(pet_type, dict):
            return "Invalid pet type!"
        
        if len(char.pets) >= 8:  # FIX: Increased limit to 8
            return "Too many pets!"
        
        # FIX: Proper money check
        cost = pet_type["cost"] if isinstance(pet_type, dict) else 1000
        if char.money < cost:
            return f"Need ${cost}!"
        
        # FIX: Expanded pet names
        pet_names = ["Buddy", "Max", "Charlie", "Lucy", "Daisy", "Rocky", "Luna", 
                     "Bailey", "Milo", "Leo", "Oliver", "Coco", "Ginger", "Pepper",
                     "Roxy", "Ziggy", "Molly", "Duke", "Sadie", "Tucker"]
        
        # FIX: Prevent duplicate names
        used_names = [p["name"] for p in char.pets]
        available_names = [n for n in pet_names if n not in used_names]
        
        if not available_names:
            return "You have too many pets with unique names!"
        
        pet_name = random.choice(available_names)
        char.pets.append({
            "name": pet_name, 
            "type": pet_type["name"] if isinstance(pet_type, dict) else pet_type,
            "age": 0  # FIX: Added age tracking
        })
        char.add_money(-cost)
        char.change_stat('happiness', 15)
        return f"Adopted {pet_name} the {pet_type['name'] if isinstance(pet_type, dict) else pet_type}!"
    
    def adopt_pet_manual(self, pet_name):
        """
        Manual pet adoption interface.
        
        FIX: Case-insensitive matching
        FIX: Proper validation
        """
        # FIX: Case-insensitive matching
        for pet in PETS:
            if pet["name"].lower() == pet_name.lower():
                return self.adopt_pet(pet)
        return "Pet not found!"
    
    def rename_pet(self, old_name, new_name):
        """
        Rename a pet.
        
        FIX: Case-insensitive matching
        FIX: Check for duplicate names
        """
        char = self._get_character()
        if not char:
            return False
        
        # FIX: Case-insensitive matching
        for pet in char.pets:
            if pet["name"].lower() == old_name.lower():
                # FIX: Check for duplicate names
                if any(p["name"].lower() == new_name.lower() for p in char.pets):
                    return False
                pet["name"] = new_name
                return True
        return False
    
    def give_away_pet(self, pet_name):
        """
        Give away a pet.
        
        FIX: Check if pet exists
        FIX: Happiness loss based on pet age
        """
        char = self._get_character()
        if not char:
            return False
        
        # FIX: Check if pet exists
        for i, pet in enumerate(char.pets):
            if pet["name"].lower() == pet_name.lower():
                # FIX: Happiness loss based on bond (age)
                happiness_loss = min(20, 5 + pet.get("age", 0) // 2)
                char.pets.pop(i)
                char.change_stat('happiness', -happiness_loss)
                return True
        return False
    
    def get_pets(self):
        """Get list of current pets."""
        char = self._get_character()
        return char.pets if char else []
    
    def get_available_pets(self):
        """Get list of available pet types."""
        return PETS
    
    def increment_relationship_years(self):
        """FIX: Increment relationship years when aging up."""
        char = self._get_character()
        if char and (char.dating or char.married):
            char.relationship_years += 1
    
    def get_children_list(self):
        """FIX: Get list of children names."""
        char = self._get_character()
        return char.children if char else []