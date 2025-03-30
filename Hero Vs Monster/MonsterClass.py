import random

# Construction of the Monster class
class Monster:
    def __init__(self):
        self.nameList = ["Goblin", "Orc", "Vampire"]
        self.health = random.randint(5, 10)
        self.strength = random.randint(1, 3)
        self.name = random.choice(self.nameList)
        self.armor = random.randint(10, 15)
        self.experience = self.health
        self.isDefeated = False
        self.initiative = 0
        self.level = 0

    # This method will be called when self.health =< 0
    def defeat(self):
        print(f"You've defeated the {self.name} and have gained {self.experience} experience!")
        self.isDefeated = True
        return self.isDefeated

    # This method is used to reduce health when attacked successfully
    def damaged(self, attack):
        self.health = self.health - attack
        if self.health <= 0:
            self.defeat()

    # This method is to roll attack and try to damage the hero
    def attack(self):
        self.damage = random.randint(1, 4)
        return self.damage
    
    # This method is to roll attack and try to damage the hero
    def aimAttack(self):
        self.aim = random.randint(1, 20) + self.strength
        return self.aim

    def rollInitiative(self):
        self.initiative = random.randint(1, 20) + self.strength
        return self.initiative