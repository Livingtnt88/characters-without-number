# Characters without number is a simple character builder for stars without number 
# and worlds without number
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
        self.modifiers = {'skill': [], 'attribute':[]}
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
            self.add_modifier(background.free_skill ,'background')
            for pick, table in self.choices['background']:
                if table == 'growth':
                    self.add_modifier(background.growth[pick], 'background')
                elif table == 'learning':
                    self.add_modifier(background.learning[pick], 'background')
        
        self.Class = Class
        self.abilities += Class.ability
        self.add_modifier(Class.modifiers, Class.name)

        self.foci = foci
        for focus in foci:
            self.add_modifier(focus.modifiers, focus.name)

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
            
    def add_modifier(self, modifier: list, source: str):
        match modifier:
            # multiple modifiers
            case [*lists] if type(lists[0]) == list:
                for list in lists:
                    self.add_modifier(list, source)
            # prerequisite
            case ['prerequisite', prerequisite, list_modifiers]:
                self.modifiers['prerequisite'] += [[prerequisite, list_modifiers, source]]
            # choice
            case ['choice', num_choices, replacement, list_modifiers]:
                self.modifiers['choice'] += [[num_choices, replacement, list_modifiers, source]]
            # ability
            case ['ability', ability]:
                self.modifiers['choice'] += [[ability, source]]
            # resource
            case ['resource', name, formula, usage]:
                self.modifiers['resource'] += [[name, formula, usage, source]]   
            # skill gain
            case ['skill', 'gain', skill]:
                self.modifiers['skill'] += [['gain', skill, source]]
            # new skill
            case ['skill', 'new', skill, type]:
                self.modifiers['skill'] += [['new', skill, type, source]]
            # skill dice
            case ['skill', 'dice', dice]:
                self.modifiers['skill'] += [['dice', dice, source]]
            # attribute score bonus
            case ['attribute', 'score', attribute, bonus]:
                self.modifiers['attribute'] += [['score', attribute, bonus, source]]
            # attribute mod bonus
            case ['attribute', 'mod', attribute, bonus]:
                 self.modifiers['attribute'] += [['mod', attribute, bonus, source]]    
            case _:
                if type(modifier) == list :
                    raise ValueError(f'Malformed/unsupported modifier {modifier} from {source}')
                else:
                    raise TypeError(f'Modifiers must be lists {modifier} from {source} is a {type(modifier)}')

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

class ability:
    pass

class foci(ability):
    def __init__(self, name: str, description: str, level: int, modifiers, tags: list = None):
        self.name = name
        self.description = description
        self.level = level

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