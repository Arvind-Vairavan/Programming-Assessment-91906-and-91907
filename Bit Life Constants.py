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
    "Millionaire": lambda c: c.money >= 1000000,
    "Scholar": lambda c: c.education == "PhD",
    "Family Person": lambda c: len(c.children) >= 3,
    "Centenarian": lambda c: c.age >= 100,
    "Career Master": lambda c: c.job in ["CEO", "Doctor"],
    "Pet Lover": lambda c: len(c.pets) >= 3,
}