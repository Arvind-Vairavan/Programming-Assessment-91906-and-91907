"""
Constants and configuration data for the BitLife game.
All game data is centralized here for easy modification and expansion.
"""

# Dictionary defining all jobs in the game with their annual salary
JOBS = {
    "Retail": {"salary": 25000},      # Entry-level job, no education needed
    "Teacher": {"salary": 45000},     # Requires bachelor's degree
    "Developer": {"salary": 85000},   # Tech job, bachelor's required
    "Doctor": {"salary": 120000},     # High-paying medical profession
    "CEO": {"salary": 200000},        # Top executive position
    "Artist": {"salary": 55000},      # Creative profession
    "Chef": {"salary": 40000},        # Culinary profession
    "Musician": {"salary": 65000},    # Entertainment industry
    "Athlete": {"salary": 150000},    # Sports professional
}

# List of available pet types with their adoption costs
PETS = [
    {"name": "Dog", "cost": 500},     # Most popular pet
    {"name": "Cat", "cost": 300},     # Independent pet
    {"name": "Bird", "cost": 100},    # Small and affordable
    {"name": "Fish", "cost": 50},     # Cheapest pet
    {"name": "Hamster", "cost": 80},  # Small rodent
    {"name": "Rabbit", "cost": 120},  # New pet option
    {"name": "Turtle", "cost": 150},  # New pet option
]

# Criminal activities with reward money and risk percentage
CRIMES = [
    {"name": "Theft", "reward": 200, "risk": 20},          # Low-risk, low-reward
    {"name": "Robbery", "reward": 500, "risk": 30},        # Medium risk/reward
    {"name": "Grand Theft Auto", "reward": 2000, "risk": 40}, # High reward
    {"name": "Bank Robbery", "reward": 5000, "risk": 60},  # Highest risk/reward
    {"name": "Cyber Crime", "reward": 3000, "risk": 35},   # Tech crime
    {"name": "Arson", "reward": 1500, "risk": 45},         # Destructive crime
]

# Names for various NPC types
MALE_NAMES = ["Alex", "Jordan", "Taylor", "Morgan", "Casey", "Riley", "Drew", "Avery"]
FEMALE_NAMES = ["Emma", "Sophia", "Olivia", "Ava", "Mia", "Charlotte", "Amelia", "Harper"]
CHILD_NAMES = ["Emma", "Liam", "Olivia", "Noah", "Sophia", "Oliver", "Ava", "Mason", "Charlotte", "Lucas"]
FRIEND_NAMES = ["Emma", "Liam", "Olivia", "Noah", "Sophia", "Oliver", "Ava", "Mason", "Charlotte", "Lucas", "Amelia", "Ethan"]