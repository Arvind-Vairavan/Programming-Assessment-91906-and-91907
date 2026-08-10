"""
Taking out the uneeded stuff final final version 
"""


import random
from data.constants import JOBS


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
        # Work button should also increase experience
        char.job_experience += 1
        return f"Worked and earned ${earned:,}"
    
    def promote_manual(self):
        char = self._get_character()
        if not char:
            return "No character found!"
        
        if not char.job:
            return "No job!"
        if char.job_experience < 36:
            return f"Need 3+ years experience! (Current: {char.job_experience} years)"
        if char.smarts < 70:
            return "Need 70+ smarts!"
        
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
        # Keep experience when resigning (character can return to same career later)
        return f"Resigned from {old}"
    
    def get_career_info(self):
        char = self._get_character()
        if not char:
            return "No character found"
        
        if not char.job:
            return "No current job"
        
        return f"{char.job}\nExperience: {char.job_experience} years\nSalary: ${JOBS[char.job]['salary']:,}"
    
    def get_job_salary(self, job_name):
        return JOBS.get(job_name, {}).get('salary', 0)
    
    def is_employed(self):
        char = self._get_character()
        return char is not None and char.job is not None
    
    def get_available_jobs(self):
        return list(JOBS.keys())
    
    def pay_yearly_salary(self):
        """Pay yearly salary to character when aging up"""
        char = self._get_character()
        if not char or not char.job:
            return 0
        
        salary = JOBS[char.job]["salary"]
        char.add_money(salary)
        return salary