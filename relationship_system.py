"""
Version One 

This is what I planned to put in side the relationships component
Relationship system managing dating, marriage, children, and pets.

There are quite a few bugs that I will probably not come around to fix but hopefully I will fix most of the bugs
"""

import random
from data.constants import MALE_NAMES, FEMALE_NAMES, CHILD_NAMES, PETS


class RelationshipSystem:
    """
    Manages all relationship-related logic.
    
    BUG: _get_character() called multiple times unnecessarily
    BUG: No validation for age in dating
    BUG: Marriage proposal can happen without dating partner existing
    BUG: Child birth doesn't check if spouse exists
    BUG: Pets don't have proper age tracking
    """
    
    def __init__(self, game):
        self.game = game
    
    def _get_character(self):
        """Get the current character."""
        return self.game.character if self.game.has_character() else None
    
    def start_dating(self, partner_name=None):
        """
        Start a romantic relationship with someone.
        
        BUG: Doesn't check if partner_name is valid
        BUG: Random partner selection doesn't consider character age
        BUG: No cooldown period after breakup
        BUG: Success rate always 60% regardless of stats
        """
        char = self._get_character()
        if not char:
            return "No character found!"
        
        # BUG: Doesn't check if partner is too young/old
        if char.dating or char.married:
            return "Already in a relationship!"
        
        if partner_name is None:
            # BUG: Random name may not match gender preference
            if char.gender == "Male":
                partner_name = random.choice(FEMALE_NAMES)
            else:
                partner_name = random.choice(MALE_NAMES)
        
        # BUG: Hardcoded 60% success rate regardless of charisma
        if random.random() < 0.6:
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
        
        BUG: Doesn't check if partner is still alive
        BUG: No engagement period
        BUG: Happiness change is always 25 regardless of partner compatibility
        BUG: Relationship years reset to 0 after marriage
        """
        char = self._get_character()
        if not char:
            return "No character found!"
        
        # BUG: Doesn't check if partner is the same gender (if not allowed)
        if not char.dating:
            return "Not dating anyone!"
        
        if random.random() < 0.6:
            char.married = True
            # BUG: Happiness boost always 25 even for forced marriages
            char.change_stat('happiness', 25)
            return f"Married {char.spouse}!"
        else:
            # BUG: Pronoun selection only handles male/female
            if char.gender == "Male":
                pronoun = "she"
            else:
                pronoun = "he"
            return f"{char.spouse} said {pronoun} is not ready yet."
    
    def marry_manual(self):
        """Manual marriage interface."""
        return self.get_married()
    
    def break_up(self):
        """
        End current relationship.
        
        BUG: Doesn't handle child custody
        BUG: No alimony payment
        BUG: Happiness loss always 20 regardless of relationship length
        BUG: Doesn't remove partner's references
        """
        char = self._get_character()
        if not char:
            return "No character found!"
        
        if not char.dating and not char.married:
            return "Not in a relationship!"
        
        name = char.spouse
        char.married = False
        char.dating = False
        char.spouse = None
        char.relationship_years = 0
        # BUG: Happiness loss is always 20
        char.change_stat('happiness', -20)
        return f"Broke up with {name}"
    
    def break_up_manual(self):
        """Manual breakup interface."""
        return self.break_up()
    
    def have_child(self):
        """
        Have a child (requires marriage and appropriate age).
        
        BUG: Doesn't check if spouse exists (only checks marriage flag)
        BUG: No fertility check based on age
        BUG: Child always gets a random name without family options
        BUG: No cost for raising child (only birth cost)
        """
        char = self._get_character()
        if not char:
            return "No character found!"
        
        # BUG: Only checks marriage flag, not if spouse exists
        if not char.married:
            return "Must be married!"
        
        # BUG: Hardcoded 4 child limit
        if len(char.children) >= 4:
            return "You have enough children!"
        
        # BUG: Men can have children at older ages in real life
        if char.age < 20 or char.age > 45:
            return "Not at the right age for children!"
        
        child = random.choice(CHILD_NAMES)
        char.children.append(child)
        char.add_money(-10000)
        char.change_stat('happiness', 20)
        return f"Welcome, {child}!"
    
    def have_child_manual(self):
        """Manual child birth interface."""
        return self.have_child()
    
    def get_relationship_status(self):
        """
        Get formatted relationship status.
        
        BUG: Relationship years not incrementing
        BUG: Shows "Dating" even if married (order issue)
        """
        char = self._get_character()
        if not char:
            return "No character"
        
        # BUG: Marriage should be checked before dating
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
        
        BUG: Pet name generation is limited to 7 names
        BUG: No check if pet_type exists in PETS
        BUG: Pet doesn't have age or happiness stats
        BUG: Can adopt the same pet name multiple times
        """
        char = self._get_character()
        if not char:
            return "No character found!"
        
        # BUG: Hardcoded pet limit of 5
        if len(char.pets) >= 5:
            return "Too many pets!"
        
        # BUG: Doesn't check if money is sufficient properly
        if char.money < pet_type["cost"]:
            return f"Need ${pet_type['cost']}!"
        
        # BUG: Pet names are hardcoded and limited
        pet_name = random.choice(["Buddy", "Max", "Charlie", "Lucy", "Daisy", "Rocky", "Luna"])
        char.pets.append({"name": pet_name, "type": pet_type["name"]})
        char.add_money(-pet_type["cost"])
        char.change_stat('happiness', 15)
        return f"Adopted {pet_name} the {pet_type['name']}!"
    
    def adopt_pet_manual(self, pet_name):
        """
        Manual pet adoption interface.
        
        BUG: Doesn't handle case sensitivity
        BUG: No validation that pet_name is valid
        """
        for pet in PETS:
            if pet["name"] == pet_name:
                return self.adopt_pet(pet)
        return "Pet not found!"
    
    def rename_pet(self, old_name, new_name):
        """
        Rename a pet.
        
        BUG: Doesn't check if new_name already exists
        BUG: Case sensitivity issues
        """
        char = self._get_character()
        if not char:
            return False
        
        for pet in char.pets:
            if pet["name"] == old_name:
                pet["name"] = new_name
                return True
        return False
    
    def give_away_pet(self, pet_name):
        """
        Give away a pet.
        
        BUG: No check if pet exists before removing
        BUG: Happiness loss always -5 regardless of bond
        """
        char = self._get_character()
        if not char:
            return False
        
        for i, pet in enumerate(char.pets):
            if pet["name"] == pet_name:
                char.pets.pop(i)
                char.change_stat('happiness', -5)
                return True
        return False
    
    def get_pets(self):
        """Get list of current pets."""
        char = self._get_character()
        return char.pets if char else []
    
    def get_available_pets(self):
        """Get list of available pet types."""
        return PETS