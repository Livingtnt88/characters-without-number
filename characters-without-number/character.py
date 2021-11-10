import random
from __future__ import annotations

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
    def __init__(self, name: str, description: str, ability, modifiers):
        self.name = name
        self.description = description

        self.ability = ability
        self.modifiers = modifiers
    
    def __add__(self, other: Class) -> Class:
        if (type(self) == type(other)) and not (self == other):
            name = f'{self.name}/{other.name}'
            description = f'{self.description}/n{other.description}'

            ability = self.ability + other.ability
            modifiers = self.modifiers + other.modifiers

            return Class(name, description, ability, modifiers)        
        else:
            raise TypeError

    def __eq__(self, other: Class) -> bool:
        if type(self) == type(other):
            if self.name == other.name and self.modifiers == other.modifiers:
                return True
            else:
                return False
        else:
            return False

class foci:
    def __init__(self, name, description, modifiers):
        self.name = name
        self.description = description

        self.modifiers = modifiers