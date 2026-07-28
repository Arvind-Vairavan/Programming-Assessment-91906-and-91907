'''
I have just done a few alterations to this class as I have decided to remove some stuff, and I wont be doing some things that I thought I was gong to do,  later on
'''

import random

class Character:
    def __init__(self, name, gender):
        self.name = name
        self.gender = gender
        self.age = 18
        self.happiness = random.randint(50, 80)
        self.health = random.randint(50, 90)
        self.smarts = random.randint(40, 80)
        self.looks = random.randint(40, 80)
        self.money = random.randint(1000, 5000)
        self.job = None
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
        self.skills = {"Coding": 0, "Art": 0, "Music": 0, "Sports": 0, "Cooking": 0}
        self.pets = []
        self.house = None
        self.car = None
        self.health_conditions = []
        self.exercise_frequency = 0
        self.diet_quality = "Average"
        self.vacations = []
        self.crimes_committed = []
        
    def to_dict(self):
        return {k: v for k, v in self.__dict__.items()}