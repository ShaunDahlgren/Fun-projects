import random
import time

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


def main():
    Enemy = Monster()
    Player = Hero("The Guy")
    dayIsSaved = False

    print(f"{Player.name} encounters a {Enemy.name}!")
    print(f"{Player.name} Health: {Player.health}, Armor: {Player.armor}")
    print(f"{Enemy.name} Health: {Enemy.health}, Armor: {Enemy.armor}\n")

    while not Player.isDefeated and not dayIsSaved:
        # Roll initiative
        Player.initiative = random.randint(1, 20) + Player.strength
        Enemy.initiative = random.randint(1, 20) + Enemy.strength
        
        if Player.initiative >= Enemy.initiative:
            print(f"{Player.name} attacks first!")
            damage = Player.attack()
            print(f"{Player.name} attacks the {Enemy.name} for {damage} damage!")
            Enemy.damaged(damage)

            if Enemy.isDefeated:
                Player.experience += Enemy.experience
                Enemy = Monster()
                print(f"{Player.name} encounters a new {Enemy.name}!")
                break

            # Enemy attacks back
            damage = Enemy.attack()
            print(f"{Enemy.name} attacks {Player.name} for {damage} damage!")
            Player.damaged(damage)

            if Player.isDefeated:
                break
        else:
            print(f"{Enemy.name} attacks first!")
            # Enemy attacks first
            damage = Enemy.attack()
            print(f"{Enemy.name} attacks {Player.name} for {damage} damage!")
            Player.damaged(damage)
                
            if Player.isDefeated:
                break
                
            damage = Player.attack()
            print(f"{Player.name} attacks the {Enemy.name} for {damage} damage!")
            Enemy.damaged(damage)
                
            if Enemy.isDefeated:
                Player.experience += Enemy.experience
            
        if random.randint(1, 20) == 20:
            print(f" {Player.name} has saved the day!")
            dayIsSaved = True
            break

        print(f"{Player.name} Health: {Player.health}")
        print(f"{Enemy.name} Health: {Enemy.health}\n")

if __name__ == "__main__":
    main()
