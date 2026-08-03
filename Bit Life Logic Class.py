'''
So what I have done is just removed the constants from this file and put them in a seperate file, so this file is just the class itself
'''

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