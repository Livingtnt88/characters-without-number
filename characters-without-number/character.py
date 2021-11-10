from __future__ import annotations
import random

def roll(number: int, dice: int, bonus: int = 0) -> int:
    sum = 0
    for x in range(number):
        sum += random.randint(1, dice)
    return sum + bonus

def roll_str(str: str) -> int:
    number, dice = str.split('d')
    try: 
        return roll(int(number), int(dice))
    except ValueError as e:
        if not dice.split('+')[-1] == '':
            dice, bonus = dice.split('+')
            return roll(int(number), int(dice), int(bonus))
        elif not dice.split('-')[-1] == '':
            dice, bonus = dice.split('-')
            return roll(int(number), int(dice), -int(bonus))
        else:
            raise e

class character:
    def __init__(self, name, attributes: dict, skill_list: dict, background: background, Class: Class, foci, items, choices: dict):
        self.name = name

        self.attributes = {}
        for attribute in attributes.keys:
            self.attributes[attribute] = [0,0]
            self.update_attribute(attribute, attributes[attribute])

        self.skills = {skill:[-1, type] for (skill, type) in skill_list.items}
        self.background = background
        self.Class = Class
        self.foci = foci
        self.items = items
        self.choices = choices
    
    def update_attribute(self, attribute: str, score: int):
        self.attributes[attribute][0] = score
        match self.attributes[attribute][0]:
                case 3:
                    self.attributes[attribute][1] = -2
                case x if x > 3 and x <= 7:
                    self.attributes[attribute][1] = -1
                case x if x > 7 and x <= 13:
                    self.attributes[attribute][1] = 0
                case x if x > 13 and x <= 17:
                    self.attributes[attribute][1] = 1
                case 18:
                    self.attributes[attribute][1] = 2

    def roll_attributes(self):
        for attribute in self.attributes.keys:
            self.update_attribute(self, attribute, roll(3,6))
            

        
class background:
    def __init__(self, name: str, description: str, free_skill: dict, quick_skills: dict, growth: list, learning: list):
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
            if self.name == other.name:
                return True
            else:
                return False
        else:
            return False

class foci:
    def __init__(self, name: str, description: str, modifiers, tags: list = None):
        self.name = name
        self.description = description

        self.modifiers = modifiers
        self.tags = tags

class item:
    def __init__(self, name: str, description: str, cost: int, enc: int, tl: int = None, packable :bool = False) -> None:
        self.name = name
        self. description = description

        self.cost = cost
        self.enc = enc
        self.packable = packable
        self.tl = tl

class armor(item):
    def __init__(self, name: str, description: str, ac: int, cost: int, enc: int, tl: int = None, ac_bonus: int = 0) -> None:
        self.ac = ac
        self.ac_bonus = ac_bonus

        super().__init__(name, description, cost, enc, tl)

class weapon(item):
    def __init__(self, name: str, description: str, damage: str, attribute: str, cost: int, enc: int, tl: int = None) -> None:
        self.damage = damage
        self.attribute = attribute
        super().__init__(name, description, cost, enc, tl)

class ranged(weapon):
    def __init__(self, name: str, description: str, damage: str, attribute: str, range: str, magazine: int, ammo: item, cost: int, enc: int, tl: int = None, burst: bool = False, loading: bool = False) -> None:
        self.range = range
        self.magazine = magazine
        self.ammo = ammo
        self.burst = burst
        self.loading = loading

        super().__init__(name, description, damage, attribute, cost, enc, tl)

class melee(weapon):
    def __init__(self, name: str, description: str, damage: str, attribute: str, shock_ac: int, shock_dmg: int, cost: int, enc: int, tl: int = None) -> None:
        self.shock_ac = shock_ac
        self.shock_dmg = shock_dmg
        super().__init__(name, description, damage, attribute, cost, enc, tl)

class heavy(weapon):
    def __init__(self, name: str, description: str, damage: str, attribute: str, range: str, magazine: int, ammo: item, cost: int, enc: int, tl: int = None, supression = False) -> None:
        self.range = range
        self.magazine = magazine
        self.ammo = ammo
        self.supression = supression

        super().__init__(name, description, damage, attribute, cost, enc, tl=tl)