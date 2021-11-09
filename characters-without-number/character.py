import random

class character:
    def __init__(self, attributes, skills, background, Class):
        pass

class background:
    def __init__(self, name, description, free_skill, quick_skills, growth, learning):
        self.name = name
        self.decription = description

        self.free_skill = free_skill
        self.quick_skills = quick_skills
        self.growth = growth
        self.learning = learning

    def roll_growth(self):
        return random.choice(self.growth)

    def roll_learning(self):
        return random.choice(self.learning)

class Class:
    pass
