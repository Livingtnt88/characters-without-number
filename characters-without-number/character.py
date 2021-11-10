import random
from __future__ import annotations

class character:
    def __init__(self, attributes, skills, background, Class, foci, items):
        pass

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
            if self.name == other.name and self.modifiers == other.modifiers:
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