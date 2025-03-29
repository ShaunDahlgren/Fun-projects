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

def main():
    Enemy = Monster()
    Player = Hero("The Guy")

    print(f"{Player.name} encounters a {Enemy.name}!")
    print(f"{Player.name} Health: {Player.health}, Armor: {Player.armor}")
    print(f"{Enemy.name} Health: {Enemy.health}, Armor: {Enemy.armor}\n")

    while not Player.isDefeated and not Enemy.isDefeated:
        # Player attacks first
        damage = Player.attack()
        print(f"{Player.name} attacks the {Enemy.name} for {damage} damage!")
        Enemy.damaged(damage)

        if Enemy.isDefeated:
            Player.experience += Enemy.experience
            break

        # Enemy attacks back
        damage = Enemy.attack()
        print(f"{Enemy.name} attacks {Player.name} for {damage} damage!")
        Player.damaged(damage)

        if Player.isDefeated:
            break

        print(f"{Player.name} Health: {Player.health}")
        print(f"{Enemy.name} Health: {Enemy.health}\n")

if __name__ == "__main__":
    main()
