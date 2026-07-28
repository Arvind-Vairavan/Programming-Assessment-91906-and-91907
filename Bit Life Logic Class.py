'''
So this is the second version of of the Logic Class and I have decided, instead of intializing all the choices for for each component I would just make them constants, 
because having them within a class, just make the code look clunky, and inefficient, and then I would have the class just call them wherever needed. 
And what I have in the class right now, is initalizing some background info, and then some story event when conditions are met
'''

# Below are all the constants that I was intiallizing before but now I have set to global constants to be easialy accessed wherever needed
EDUCATION = ["None", "High School", "Bachelor's", "Master's", "PhD"]
JOBS = {
    "None": {"salary": 0, "requirements": "None", "min_age": 16},
    "Retail Worker": {"salary": 25000, "requirements": "High School", "min_age": 16},
    "Teacher": {"salary": 45000, "requirements": "Bachelor's", "min_age": 22},
    "Software Engineer": {"salary": 85000, "requirements": "Bachelor's", "min_age": 22},
    "Doctor": {"salary": 120000, "requirements": "Master's", "min_age": 26},
    "CEO": {"salary": 200000, "requirements": "Master's", "min_age": 30},
    "Artist": {"salary": 55000, "requirements": "Bachelor's", "min_age": 22},
    "Chef": {"salary": 40000, "requirements": "High School", "min_age": 18},
    "Pilot": {"salary": 90000, "requirements": "Bachelor's", "min_age": 24},
    "Musician": {"salary": 65000, "requirements": "High School", "min_age": 18},
    "Athlete": {"salary": 150000, "requirements": "High School", "min_age": 18},
}

PETS = [{"name": "Dog", "cost": 500}, {"name": "Cat", "cost": 300}, {"name": "Bird", "cost": 100},
        {"name": "Fish", "cost": 50}, {"name": "Hamster", "cost": 80}
]

HOUSES = [{"name": "Studio", "cost": 100000}, {"name": "Apartment", "cost": 200000},
          {"name": "House", "cost": 350000}, {"name": "Mansion", "cost": 1000000},
          {"name": "Castle", "cost": 5000000}
]

CARS = [{"name": "Used Sedan", "cost": 5000}, {"name": "New Sedan", "cost": 25000},
        {"name": "SUV", "cost": 40000}, {"name": "Sports Car", "cost": 80000},
        {"name": "Luxury Car", "cost": 150000}, {"name": "Supercar", "cost": 300000}
]

VACATIONS = [{"name": "Paris", "cost": 3000, "happiness": 30}, {"name": "Bali", "cost": 2500, "happiness": 35},
             {"name": "New York", "cost": 3500, "happiness": 25}, {"name": "Tokyo", "cost": 4000, "happiness": 30},
             {"name": "Santorini", "cost": 2800, "happiness": 40}, {"name": "Dubai", "cost": 5000, "happiness": 35},
             {"name": "Swiss Alps", "cost": 3200, "happiness": 38}, {"name": "Maldives", "cost": 4500, "happiness": 45},
             {"name": "Rome", "cost": 2800, "happiness": 28}, {"name": "Thailand", "cost": 2000, "happiness": 32}
]

CRIMES = [{"name": "Shop Theft", "reward": 200, "risk": 20, "jail_time": 0.5},
          {"name": "Pickpocketing", "reward": 500, "risk": 30, "jail_time": 1},
          {"name": "Grand Theft Auto", "reward": 2000, "risk": 40, "jail_time": 2},
          {"name": "Bank Robbery", "reward": 5000, "risk": 60, "jail_time": 5},
          {"name": "Diamond Heist", "reward": 10000, "risk": 75, "jail_time": 8},
          {"name": "Hacking", "reward": 3000, "risk": 35, "jail_time": 3},
          {"name": "Arson", "reward": 1500, "risk": 45, "jail_time": 4},
          {"name": "Drug Trafficking", "reward": 8000, "risk": 70, "jail_time": 7}
]

LOTTERY = [{"name": "Small Prize", "amount": 100, "chance": 0.40},
           {"name": "Medium Prize", "amount": 1000, "chance": 0.25},
           {"name": "Big Prize", "amount": 10000, "chance": 0.15},
           {"name": "Jackpot!", "amount": 100000, "chance": 0.05}
]

ACHIEVEMENTS = {
    "Millionaire": lambda character: character.money >= 1000000,
    "Scholar": lambda character: character.education == "PhD",
    "Family Person": lambda character: len(character.children) >= 3,
    "Centenarian": lambda character: character.age >= 100,
    "Career Master": lambda character: character.job == "CEO",
    "Pet Lover": lambda character: len(character.pets) >= 3,
    "Car Owner": lambda character: character.car is not None,
    "Home Owner": lambda character: character.house is not None,
    "World Traveler": lambda character: len(character.vacations) >= 3,
    "Criminal": lambda character: len(character.crimes_committed) >= 3,
    "Lottery Winner": lambda character: character.lottery_won,
}

class Logic:
    def __init__(self):
        self.character = None
        self.achievements = []
        self.year = 2026
        self.story_events = [
            # this is what happens in one block
            #This Python dictionary entry has an event trigger it only activates when a character turns 20 years old and has no prior education. 
            # Once those conditions are met, it gives the player with three choices.
            # Each choice is paired with an internal function.
            # So basically it acts as a life-event decision to improve and further grow the player's background
            {'trigger': lambda character: character.age == 20 and character.education == "None",
             'choices': [
                 ("Go to college", self._go_to_college),
                 ("Start working", self._start_working),
                 ("Travel the world", self._travel_world)]},
            {'trigger': lambda character: character.age == 25 and not character.married and character.happiness > 60,
             'choices': [
                 ("Look for love", self._find_love),
                 ("Focus on career", self._focus_career),
                 ("Adopt a pet", self._adopt_pet)]},
            {'trigger': lambda character: character.age == 30 and character.money > 50000 and character.house is None,
             'choices': [
                 ("Buy a house", self._buy_house),
                 ("Invest in stocks", self._invest_stocks),
                 ("Start a business", self._start_business)]},
            {'trigger': lambda character: character.age == 35 and character.married and not character.children,
             'choices': [
                 ("Have a baby", self._have_baby),
                 ("Adopt a child", self._adopt_child),
                 ("Focus on career", self._focus_career)]},
            {'trigger': lambda character: character.age == 40 and character.stress > 70,
             'choices': [
                 ("Take a vacation", self._take_vacation),
                 ("Change career", self._change_career),
                 ("Start a hobby", self._start_hobby)]},
            {'trigger': lambda character: character.age == 50 and character.money > 200000,
             'choices': [
                 ("Retire early", self._retire_early),
                 ("Start a charity", self._start_charity),
                 ("Write a book", self._write_book)]}
        ]