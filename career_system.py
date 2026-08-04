"""
Version 2 now, I added the promotion system because people wanted to actually progress in their careers. 
You can request a promotion but it's pretty strict - need 3 years experience and 70 smarts. 
The salary goes up by 20% when you get promoted which is nice. Still pretty basic but at least there's something to work towards now.

This version WORKS for the most part but there's a bug I noticed - the promotion doesn't check if you've already been promoted recently 
so you could theoretically get promoted every single year. Also the error messages are pretty vague, 
just saying "Need 3+ years experience" without telling you exactly how much more you need.
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
    
    def promote_manual(self):
        char = self._get_character()
        if not char:
            return "No character found!"
        
        if not char.job:
            return "No job!"
    
        if char.job_experience < 36:
            return "Need 3+ years experience!"
        
        if char.smarts < 70:
            return "Need 70+ smarts!"
        
        # BUG: No cooldown check! You can get promoted every year
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
    
    def get_available_jobs(self):
        return list(JOBS.keys())


if __name__ == "__main__":
    print("VERSION 2 TEST")
    print("-" * 40)
    
    # Test 1: Normal promotion (should work)
    print("TEST 1: Normal promotion with enough experience")
    char = Character("Alice", "Female")
    char.job = "Developer"
    char.job_experience = 36
    char.smarts = 80
    game = MockGame(char)
    career = CareerSystem(game)
    
    print("Experience:", char.job_experience, "months")
    print("Smarts:", char.smarts)
    print("Current salary:", JOBS[char.job]["salary"])
    result = career.promote_manual()
    print("Result:", result)
    print("New salary:", JOBS[char.job]["salary"])
    print("Last promotion age:", char.last_promotion_age)
    print()
    
    # Test 2: Promotion without enough experience (should fail)
    print("TEST 2: Not enough experience")
    char2 = Character("Bob", "Male")
    char2.job = "Teacher"
    char2.job_experience = 24
    char2.smarts = 75
    game2 = MockGame(char2)
    career2 = CareerSystem(game2)
    
    print("Experience:", char2.job_experience, "months")
    print("Smarts:", char2.smarts)
    result = career2.promote_manual()
    print("Result:", result)
    print()
    
    # Test 3: Promotion without enough smarts (should fail)
    print("TEST 3: Not enough smarts")
    char3 = Character("Carol", "Female")
    char3.job = "Doctor"
    char3.job_experience = 48
    char3.smarts = 55
    game3 = MockGame(char3)
    career3 = CareerSystem(game3)
    
    print("Experience:", char3.job_experience, "months")
    print("Smarts:", char3.smarts)
    result = career3.promote_manual()
    print("Result:", result)
    print()
    
    # Test 4: BUG - Promotion cooldown issue
    print("TEST 4: BUG - Promotion cooldown not working")
    char4 = Character("Dave", "Male")
    char4.job = "CEO"
    char4.job_experience = 60
    char4.smarts = 90
    char4.age = 25
    char4.last_promotion_age = 25
    game4 = MockGame(char4)
    career4 = CareerSystem(game4)
    
    print("Age:", char4.age)
    print("Last promotion age:", char4.last_promotion_age)
    print("Current salary:", JOBS[char4.job]["salary"])
    result = career4.promote_manual()
    print("Result:", result)
    print("New salary:", JOBS[char4.job]["salary"])
    print("BUG: Got promoted again immediately! Should have a cooldown.")