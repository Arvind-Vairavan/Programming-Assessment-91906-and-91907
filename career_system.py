"""
Alright so this is version 1 of the career system, literally just the bare minimum to get jobs working. 
You can get a random job, work to earn money, and quit. That's it. No promotions, no experience tracking that matters, 
nothing fancy. Just a basic system to test if the game can handle having a job at all.

This version WORKS as expected. The find_job() assigns a random job, work() calculates earnings and updates stats, 
resign() clears the job. All basic functionality is solid. No bugs to fix yet because there's barely any features.
"""

import random

JOBS = {
    "Retail": {"salary": 25000},      
    "Teacher": {"salary": 45000},     
    "Developer": {"salary": 85000},   
    "Doctor": {"salary": 120000},     
    "CEO": {"salary": 200000},        
    "Artist": {"salary": 55000},      
    "Chef": {"salary": 40000},        
    "Musician": {"salary": 65000},    
    "Athlete": {"salary": 150000},    
}


class Character:
    
    def __init__(self, name, gender):
        self.name = name
        self.gender = gender
        
        self.age = 18
        self.money = random.randint(1000, 5000)
        self.happiness = random.randint(50, 80)
        self.health = random.randint(50, 90)
        self.smarts = random.randint(40, 80)
        self.stress = random.randint(20, 50)
        self.social = random.randint(30, 70)
        
        self.job = None
        self.job_experience = 0
        self.last_promotion_age = 0
        
        self.married = False
        self.spouse = None
        self.children = []
        self.dating = False
        self.relationship_years = 0
        self.last_relationship_event = 0
        self.friends = []
        
        self.pets = []
        self.house = None
        self.car = None
        self.vacations = 0
        
        self.crimes = 0
        self.criminal_record = False
        
        self.alive = True
        self.achievements_earned = []

    def change_stat(self, stat, amount):
        if hasattr(self, stat):
            current = getattr(self, stat)
            if isinstance(current, (int, float)):
                setattr(self, stat, max(0, min(100, current + amount)))

    def add_money(self, amount):
        self.money = max(0, self.money + amount)

    def to_dict(self):
        return {k: v for k, v in self.__dict__.items()}

    @classmethod
    def from_dict(cls, data):
        char = cls(data['name'], data['gender'])
        for key, value in data.items():
            if hasattr(char, key):
                setattr(char, key, value)
        return char


class MockGame:
    def __init__(self, char): 
        self.character = char
    
    def has_character(self): 
        return self.character is not None


class CareerSystem:
    
    def __init__(self, game):
        self.game = game
    
    def _get_character(self):
        return self.game.character if self.game.has_character() else None
    
    def find_job(self):
        char = self._get_character()
        if not char:
            return "No character found!"
        
        available = list(JOBS.keys())
        if not available:
            return "No jobs available!"
        
        char.job = random.choice(available)
        char.job_experience = 0
        return f"Started as {char.job}!"
    
    def work(self):
        char = self._get_character()
        if not char:
            return "No character found!"
        
        if not char.job:
            return "No job!"
        
        earned = JOBS[char.job]["salary"] // 12 + random.randint(-500, 2000)
        char.add_money(max(0, earned))
        char.change_stat('happiness', -3)
        char.change_stat('stress', 5)
        char.job_experience += 1
        return f"Worked and earned ${earned:,}"
    
    def resign(self):
        char = self._get_character()
        if not char:
            return "No character found!"
        
        if not char.job:
            return "No job!"
        
        old = char.job
        char.job = None
        char.job_experience = 0
        return f"Resigned from {old}"
    
    def get_career_info(self):
        char = self._get_character()
        if not char:
            return "No character found"
        
        if not char.job:
            return "No current job"
        
        return f"{char.job}\nExperience: {char.job_experience//12} years\nSalary: ${JOBS[char.job]['salary']:,}"
    
    def get_available_jobs(self):
        return list(JOBS.keys())


# VERSION 1 TEST - RUN THIS TO SEE IT WORKS
if __name__ == "__main__":
    print("VERSION 1 TEST")
    print("-" * 40)
    
    # Create character and career
    char = Character("Bob", "Male")
    game = MockGame(char)
    career = CareerSystem(game)
    
    # Test find job
    print("Finding job:")
    result = career.find_job()
    print("Result:", result)
    print("Job:", char.job)
    print("Experience:", char.job_experience)
    print()
    
    # Test work
    print("Working:")
    result = career.work()
    print("Result:", result)
    print("Money:", char.money)
    print("Happiness:", char.happiness)
    print("Stress:", char.stress)
    print("Experience:", char.job_experience)
    print()
    
    # Test work again
    print("Working again:")
    result = career.work()
    print("Result:", result)
    print("Money:", char.money)
    print("Experience:", char.job_experience)
    print()
    
    # Test career info
    print("Career info:")
    print(career.get_career_info())
    print()
    
    # Test resign
    print("Resigning:")
    result = career.resign()
    print("Result:", result)
    print("Job:", char.job)
    print("Experience:", char.job_experience)