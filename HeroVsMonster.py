import random

class Hero:
    def __init__(self, name):
        pass

    health = 10
    strength = random.randint(1, 5)

class Monster:
    def __init__(self):
        pass
    
    nameList = ["Goblin", "Orc", "Vampire"]
    health = random.randint(1, 10)
    strength = random.randint(1, 3)
    name = random.choice(nameList)

    def defeat():
        print(f"You've defeated the {self.name}")

    def damaged(attack):
        