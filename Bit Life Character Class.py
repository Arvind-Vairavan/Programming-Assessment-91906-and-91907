'''
So in this version of the the character class is just where I add, what I think are a few more helpful function that should go in this class
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
        self.alive = True
        self.events = [f"Born as {gender}"]
        self.stress = random.randint(20, 50)
        self.social = random.randint(30, 70)
        self.criminal_record = False
        self.pets = []
        self.house = None
        self.car = None
        self.vacations = []
        self.crimes_committed = []
        self.lottery_won = False

    def change_stat(self, stat, amount):
        if stat in self.__dict__:
            self.__dict__[stat] = max(0, min(100, self.__dict__[stat] + amount))

    def add_event(self, message):
        self.events.append(message)

    def add_money(self, amount):
        self.money = max(0, self.money + amount)

    def to_dict(self):
        return self.__dict__.copy()

def character_from_dict(data):
    char = Character(data["name"], data["gender"])
    char.__dict__.update(data)
    return char