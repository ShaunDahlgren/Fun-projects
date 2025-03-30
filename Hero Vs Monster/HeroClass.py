import random

# Construction of the Hero class
class Hero:
    def __init__(self, name):
        self.name = name
        self.health = 10
        self.strength = random.randint(1, 5)
        self.armor = random.randint(11, 18)
        self.experience = 0
        self.isDefeated = False
        self.aim = random.randint(1, 20) + self.strength
        self.initiative = 0

    def attack(self):
        self.damage = random.randint(1, 6)
        return self.damage

    def defeat(self):
        print(f"{self.name} has been defeated")
        self.isDefeated = True
        return self.isDefeated

    def damaged(self, attack):
        self.health -= attack
        if self.health <= 0:
            self.defeat()
    
    # This method is to roll attack and try to damage the hero
    def aimAttack(self):
        self.aim = random.randint(1, 20) + self.strength
        return self.aim
    
    # This is the start of the leveing system
    def gainExperience(self, exp):
        self.experience += exp
        if self.experience >= 10:
            self.levelUp()
    def levelUp(self):
        self.level += 1
        self.health += self.level
        self.strength += self.level
        self.armor += self.level
        print(f"{self.name} leveled up! New level: {self.level}")
        print(f"New stats: Health: {self.health}, Strength: {self.strength}, Armor: {self.armor}")
        
    def rollInitiative(self):
        self.initiative = random.randint(1, 20) + self.strength
        return self.initiative
    