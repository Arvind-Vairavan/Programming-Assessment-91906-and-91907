'''
In this Version of the I will be trying to incorperate my first class which is called the chracter class using an innit function, 
to initialize all the attributes a character in this game will have, I will be adding more attricute to make the game realistic as well
'''

import random

class Character:
    def __init__(self, name, gender):
        self.name = name
        self.gender = gender
        # this is the default starting age, but I said I will try to make this as close as possible to the real game,
        # but this is one the things I would like to change as nothing really happens, and nothing can really bone before the age of 18 in the game 
        self.age = 18 
        # Below are the defult ranges of of said "Stats" which as are to you as soon as you make a chracter
        self.happiness = random.randint(50, 80)
        self.health = random.randint(50, 90)
        self.smarts = random.randint(40, 80)
        self.looks = random.randint(40, 80)
        self.money = random.randint(1000, 5000)
        # And below are the rest of the attributes which have defult assinged to them  
        self.job = None
        # This is a string because I want to be able to change to what ever the player's character decide to do e.g. school, university, etc
        self.education = "None"
        self.married = False
        self.spouse = None
        self.children = []
        self.is_alive = True
        self.life_events = [f"Born as {gender}"]
        self.stress = random.randint(20, 50)
        self.social = random.randint(30, 70)
        self.criminal_record = False
        self.friends = []
        # These will be developed through gameplay which is they are set to zero, and are not something you will be given when you make your character
        self.skills = {"Coding": 0, "Art": 0, "Music": 0, "Sports": 0, "Cooking": 0}
        # This starts of empty but it is a dictionary for the reason that 
        self.relationships = {}
        self.pets = []
        self.house = None
        self.car = None
        self.health_conditions = []
        self.years_smoking = 0
        self.years_drinking = 0
        self.exercise_frequency = 0
        # This is a string because I want to be able to change is the values I want which are Poor, Average, Good, Excellent
        self.diet_quality = "Average"  