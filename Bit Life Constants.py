'''
So after some thought and consideration I have decided due to some cancelation, 
as I have changed my orginal plan as that stuff inside that plan was too long I have decided to shorten it,
which means not have as much functions and code as I originally thought I would have, 
so along with that I have decided to shorten then amount of constants I need, 
by getting rid of a few constants and shortening others
'''


JOBS = {
    "Retail": {"salary": 25000, "req": "None"},
    "Teacher": {"salary": 45000, "req": "Bachelor's"},
    "Developer": {"salary": 85000, "req": "Bachelor's"},
    "Doctor": {"salary": 120000, "req": "Master's"},
    "CEO": {"salary": 200000, "req": "Master's"},
    "Artist": {"salary": 55000, "req": "Bachelor's"},
    "Chef": {"salary": 40000, "req": "None"},
    "Musician": {"salary": 65000, "req": "None"},
    "Athlete": {"salary": 150000, "req": "None"},
}

PETS = ["Dog", "Cat", "Bird", "Fish", "Hamster"]
PET_COSTS = {"Dog": 500, "Cat": 300, "Bird": 100, "Fish": 50, "Hamster": 80}

HOUSES = [
    {"name": "Studio", "cost": 100000},
    {"name": "Apartment", "cost": 200000},
    {"name": "House", "cost": 350000},
    {"name": "Mansion", "cost": 1000000},
]

CARS = [
    {"name": "Sedan", "cost": 5000},
    {"name": "SUV", "cost": 25000},
    {"name": "Sports Car", "cost": 80000},
    {"name": "Luxury Car", "cost": 150000},
]

VACATIONS = [
    {"name": "Paris", "cost": 3000, "happiness": 30},
    {"name": "Bali", "cost": 2500, "happiness": 35},
    {"name": "Tokyo", "cost": 4000, "happiness": 30},
    {"name": "Santorini", "cost": 2800, "happiness": 40},
]

CRIMES = [
    {"name": "Theft", "reward": 200, "risk": 20},
    {"name": "Robbery", "reward": 500, "risk": 30},
    {"name": "Grand Theft Auto", "reward": 2000, "risk": 40},
    {"name": "Bank Robbery", "reward": 5000, "risk": 60},
]

ACHIEVEMENTS = {
    "Millionaire": lambda character: character.money >= 1000000,
    "Family Person": lambda character: len(character.children) >= 3,
    "Centenarian": lambda character: character.age >= 100,
    "Career Master": lambda character: character.job in ["CEO", "Doctor"],
    "Pet Lover": lambda character: len(character.pets) >= 3,
}