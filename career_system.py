"""
Version 3 is where I added proper job selection support. Before this you could only get random jobs but now you can actually choose what you want to do. 
Added helper methods to get job salaries and check employment status. This makes it way easier for the GUI to display job options to the player instead of just picking randomly.

This version WORKS fine for the new features but the promotion bug from version 2 still exists. 
I haven't fixed it yet because I was focused on adding the job selection stuff. So you can select jobs now but promotions are still broken.
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
        
        available = self.get_available_jobs()
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
        
        salary = self.get_job_salary(char.job)
        earned = salary // 12 + random.randint(-500, 2000)
        char.add_money(max(0, earned))
        char.change_stat('happiness', -3)
        char.change_stat('stress', 5)
        char.job_experience += 1
        return f"Worked and earned ${earned:,}"
    
    def promote_manual(self):
        char = self._get_character()
        if not char:
            return "No character found!"
        
        if not char.job:
            return "No job!"
        
        if char.job not in JOBS:
            return "Job not found!"
        
        if char.job_experience < 36:
            return "Need 3+ years experience!"
        
        if char.smarts < 70:
            return "Need 70+ smarts!"
        
        # BUG: Still no cooldown check!
        increase = int(JOBS[char.job]["salary"] * 0.2)
        JOBS[char.job]["salary"] += increase
        char.last_promotion_age = char.age
        return f"Promoted! Salary increased by ${increase:,}!"
    
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
    
    def get_job_salary(self, job_name):
        return JOBS.get(job_name, {}).get('salary', 0)
    
    def is_employed(self):
        char = self._get_character()
        return char is not None and char.job is not None
    
    def get_available_jobs(self):
        return list(JOBS.keys())


if __name__ == "__main__":
    print("VERSION 3 TEST")
    print("-" * 40)
    
    # Test 1: Get available jobs (NEW FEATURE)
    print("TEST 1: Get available jobs")
    char = Character("Test", "Male")
    game = MockGame(char)
    career = CareerSystem(game)
    
    jobs = career.get_available_jobs()
    print("Available jobs:", ", ".join(jobs))
    print()
    
    # Test 2: Get job salary (NEW FEATURE)
    print("TEST 2: Get job salary")
    for job in jobs[:3]:
        salary = career.get_job_salary(job)
        print(job + ":", "$" + str(salary) + "/year")
    print()
    
    # Test 3: Check employment status (NEW FEATURE)
    print("TEST 3: Employment status")
    print("Is employed?", career.is_employed())
    char.job = "Developer"
    print("After setting job...")
    print("Is employed?", career.is_employed())
    print()
    
    # Test 4: BUG - Promotion cooldown still broken
    print("TEST 4: BUG - Promotion cooldown still not working")
    char2 = Character("BugTest", "Male")
    char2.job = "Artist"
    char2.job_experience = 48
    char2.smarts = 85
    char2.age = 30
    char2.last_promotion_age = 30
    game2 = MockGame(char2)
    career2 = CareerSystem(game2)
    
    print("Age:", char2.age)
    print("Last promotion age:", char2.last_promotion_age)
    print("Current salary:", JOBS[char2.job]["salary"])
    result = career2.promote_manual()
    print("Result:", result)
    print("New salary:", JOBS[char2.job]["salary"])
    print("BUG: Still no cooldown check! Got promoted immediately.")
    print()
    
    # Test 5: BUG - Vague error messages
    print("TEST 5: BUG - Vague error messages")
    char3 = Character("ErrorTest", "Female")
    char3.job = "Doctor"
    char3.job_experience = 30
    char3.smarts = 65
    game3 = MockGame(char3)
    career3 = CareerSystem(game3)
    
    print("Experience:", char3.job_experience, "months")
    print("Smarts:", char3.smarts)
    result = career3.promote_manual()
    print("Result:", result)
    print("BUT: Doesn't tell me I need 6 more months and 5 more smarts.")