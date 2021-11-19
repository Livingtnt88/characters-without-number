# Characters without number is a simple character builder for stars without number and worlds without number
#    Copyright (C) 2021  LivingTnT88
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

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
    def __init__(self, name, attributes: dict, skill_list: dict, choices: dict, background: background, Class: Class, foci: list[foci], items):
        self.modifiers = {'prerequisite': [], 'choice': [], 'ability': [], 'resource': [], 'resource used': [], 'new skill': [], 'skill gain': [], 'skill dice': [], 'attribute score bonus': [], 'attribute mod bonus': [], 'set stat': [], 'stat modification':[]}
        self.abilities = []
        self.name = name

        self.attributes = {}
        for attribute in attributes.keys:
            self.attributes[attribute] = [0,0]
            self.update_attribute(attribute, attributes[attribute])

        self.skills = {skill:[-1,type] for (skill, type) in skill_list.items}
        self.choices = choices
        
        self.background = background
        if self.choices['background'] == 'quick_skills':
            self.add_modifier(background.quick_skills ,'background')
        else:
            self.add_modifier(background.free_skill)
            for pick, table in self.choices['background']:
                if table == 'growth':
                    self.add_modifier(background.growth[pick])
                elif table == 'learning':
                    self.add_modifier(background.learning[pick])
        
        self.Class = Class
        self.abilities += Class.ability
        self.add_modifier(Class.modifiers)

        self.foci = foci
        for focus in foci:
            self.add_modifier(focus.passive_modifiers)

        self.items = items
        
    
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
            
    def add_modifier(self, modifiers: dict):
        for type, modifier in modifiers.values:
            if type == 'modifier':
                self.add_modifier(modifier)
            elif isinstance(modifier, list):
                try:
                    self.modifiers[type].extend(modifier)
                except KeyError:
                    raise ValueError(f'unsupported modifier from {modifier[-1]}, {type}: {modifier}')
            else:
                raise TypeError(f'Modifiers must be lists {modifier} is a {type(modifier)}')


class background:
    def __init__(self, name: str, description: str, free_skill: str, quick_skills: list, growth: list, learning: list):
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
        if isinstance(other, Class) and not (self == other):
            name = f'{self.name}/{other.name}'
            description = f'{self.description}/n{other.description}'
            
            ability = self.ability + other.ability
            modifiers = self.modifiers + other.modifiers
            
            return Class(name, description, ability, modifiers)
        elif self == other:
            raise ValueError('Class can only be added with another unique Class')
        else:
            raise TypeError(f'Class can only be added with another unique Class not {type(other)}')
    
    def __eq__(self, other: Class) -> bool:
        if isinstance(other, Class):
            if self.name == other.name:
                return True
            else:
                return False
        else:
            return False
    
    def __repr__(self) -> str:
        return f'Class({self.name}, {self.description}, {self.ability}, {self.modifiers})'

class partial_class(Class):
    def __init__(self, name: str, description: str, ability, modifiers):
        super().__init__(name, description, ability, modifiers)
    
    def __repr__(self) -> str:
        return f'partial_class({self.name}, {self.description}, {self.ability}, {self.modifiers})'

class ability:
    def __init__(self, name: str,
                description: str, cost: list = None, 
                passive_modifiers: list[list] = None, 
                active_modifiers: dict[list] = None, 
                actions: list = None, 
                duration: dict[list] = None, 
                resources: dict[list] = None, 
                group: list = None
                ) -> None:
        
        self.name = name
        self.description = description

        self.cost = cost
        self.passive_modifiers = passive_modifiers
        self.active_modifiers = active_modifiers
        self.actions = actions
        self.duration = duration
        self.resources = resources
        self.group = group

    def use(self, action: str) -> tuple:
        return (self.resources[action], self.duration[action], self.active_modifiers[action])
    
class foci(ability):
   def __init__(self, name: str, 
                description: str, 
                passive_modifiers: list[list] = None, 
                active_modifiers: dict[list] = None, 
                actions: list = None, 
                duration: dict[list] = None, 
                resources: dict[list] = None, 
                group: list = None
                ) -> None:
       
       super().__init__(name, description, ['focus pick', 1], passive_modifiers, active_modifiers, actions, duration, resources, ['foci'] + group)

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