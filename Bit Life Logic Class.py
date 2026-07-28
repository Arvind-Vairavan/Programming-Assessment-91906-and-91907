'''
So this is my Logic class, Thiis is where I have intialized every thing that is going to be used inside the logic class, 
the logic class is where all the game running is going to be done, so all I have so far is that is just listing dictionaries of choices,m like choices of pets,
choices of cars, choices of house and so on
'''

class Logic:
    def __init__(self):
        self.character = None
        self.save_file = "bitlife_save.json"
        self.year = 2026
        self.achievements = []
        self.education_levels = ["None", "High School", "Bachelor's", "Master's", "PhD"]
        # So these are dictionaries nested within a dictionary, that give us information, on the salary of the jobs, the education level requirment, and the minimum age
        self.jobs = {
            "None": {"salary": 0, "requirement": "None", "min_age": 16},
            "Retail Worker": {"salary": 25000, "requirement": "High School", "min_age": 16},
            "Teacher": {"salary": 45000, "requirement": "Bachelor's", "min_age": 22},
            "Software Engineer": {"salary": 85000, "requirement": "Bachelor's", "min_age": 22},
            "Doctor": {"salary": 120000, "requirement": "Master's", "min_age": 26},
            "Scientist": {"salary": 95000, "requirement": "PhD", "min_age": 28},
            "CEO": {"salary": 200000, "requirement": "Master's", "min_age": 30},
            "Artist": {"salary": 55000, "requirement": "Bachelor's", "min_age": 22},
            "Chef": {"salary": 40000, "requirement": "High School", "min_age": 18},
            "Pilot": {"salary": 90000, "requirement": "Bachelor's", "min_age": 24},
            "Musician": {"salary": 65000, "requirement": "High School", "min_age": 18},
            "Athlete": {"salary": 150000, "requirement": "High School", "min_age": 18}
        }
        # So below are all multiple dictionaries within a list, and the value of each key is like one or two factor that you have to consider when playing 
        self.pet_types = [
            {"name": "Dog", "cost": 500},
            {"name": "Cat", "cost": 300},
            {"name": "Bird", "cost": 100},
            {"name": "Fish", "cost": 50},
            {"name": "Hamster", "cost": 80}
        ]
        self.house_types = [
            {"name": "Studio", "cost": 100000},
            {"name": "Apartment", "cost": 200000},
            {"name": "House", "cost": 350000},
            {"name": "Mansion", "cost": 1000000},
            {"name": "Castle", "cost": 5000000}
        ]
        self.car_types = [
            {"name": "Used Sedan", "cost": 5000},
            {"name": "New Sedan", "cost": 25000},
            {"name": "SUV", "cost": 40000},
            {"name": "Sports Car", "cost": 80000},
            {"name": "Luxury Car", "cost": 150000},
            {"name": "Supercar", "cost": 300000}
        ]
        self.vacation_destinations = [
            {"name": "Paris", "cost": 3000, "happiness": 30},
            {"name": "Bali", "cost": 2500, "happiness": 35},
            {"name": "New York", "cost": 3500, "happiness": 25},
            {"name": "Tokyo", "cost": 4000, "happiness": 30},
            {"name": "Santorini", "cost": 2800, "happiness": 40},
            {"name": "Dubai", "cost": 5000, "happiness": 35},
            {"name": "Swiss Alps", "cost": 3200, "happiness": 38},
            {"name": "Maldives", "cost": 4500, "happiness": 45},
            {"name": "Rome", "cost": 2800, "happiness": 28},
            {"name": "Thailand", "cost": 2000, "happiness": 32}
        ]
        self.crimes = [
            {"name": "Shop Theft", "reward": 200, "risk": 20, "jail_time": 0.5},
            {"name": "Pickpocketing", "reward": 500, "risk": 30, "jail_time": 1},
            {"name": "Grand Theft Auto", "reward": 2000, "risk": 40, "jail_time": 2},
            {"name": "Bank Robbery", "reward": 5000, "risk": 60, "jail_time": 5},
            {"name": "Diamond Heist", "reward": 10000, "risk": 75, "jail_time": 8},
            {"name": "Hacking", "reward": 3000, "risk": 35, "jail_time": 3},
            {"name": "Arson", "reward": 1500, "risk": 45, "jail_time": 4},
            {"name": "Drug Trafficking", "reward": 8000, "risk": 70, "jail_time": 7}
        ]
        self.lottery_prizes = [
            {"name": "Small Prize", "amount": 100, "chance": 0.40},
            {"name": "Medium Prize", "amount": 1000, "chance": 0.25},
            {"name": "Big Prize", "amount": 10000, "chance": 0.15},
            {"name": "Jackpot!", "amount": 100000, "chance": 0.05}
        ]
        # I am using lambda here to store these check conditions as unexecuted rules inside the dictionary, 
        # so Python doesn't try to run them before a real character even exists
        # So when I want I can loop through the list and pass a specific character into each function
        # It keeps my code clean because I can define all eleven unique achievement formulas right here without having to write separate named functions
        self.achievement_defs = {
            "Millionaire": (lambda character: character.money >= 1000000, "Millionaire!"),
            "Scholar": (lambda character: character.education == "PhD", "Scholar!"),
            "Family Person": (lambda character: len(character.children) >= 3, "Family Person!"),
            "Centenarian": (lambda character: character.age >= 100, "Centenarian!"),
            "Career Master": (lambda character: character.job == "CEO", "Career Master!"),
            "Pet Lover": (lambda character: len(character.pets) >= 3, "Pet Lover!"),
            "Car Collector": (lambda character: character.car is not None, "Car Owner!"),
            "Home Owner": (lambda character: character.house is not None, "Home Owner!"),
            "World Traveler": (lambda character: len(character.vacations) >= 3, "World Traveler!"),
            "Criminal": (lambda character: len(character.crimes_committed) >= 3, "Criminal!"),
            "Lottery Winner": (lambda character: character.lottery_won, "Lottery Winner!")
        }
        # This is is just some death cause, with some number for age and probability 
        self.death_causes = {
            "old_age": (70, ["passed away peacefully", "died of natural causes"], 1.0),
            "heart_disease": (45, ["died from a heart attack", "passed due to heart complications"], 1.5),
            "cancer": (40, ["lost battle with cancer", "passed away from cancer"], 1.3),
            "accident": (18, ["died in a car accident", "passed away in a tragic accident"], 0.3),
            "jail": (18, ["died in prison", "was killed in jail"], 0.1)
        }
        self.story_events = self.build_story_events()