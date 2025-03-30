import random
from HeroClass import Hero
from MonsterClass import Monster

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
