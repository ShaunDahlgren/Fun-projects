import random
from HeroClass import Hero
from MonsterClass import Monster
from BattleClass import Battle

def main():
    Enemy = Monster()
    Player = Hero("The Guy")

    print(f"{Player.name} encounters a {Enemy.name}!")
    print(f"{Player.name} Health: {Player.health}, Armor: {Player.armor}")
    print(f"{Enemy.name} Health: {Enemy.health}, Armor: {Enemy.armor}\n")

    while Player.level <= 10 and not Player.isDefeated:
        battle = Battle()
        battle.battleStart(Player, Enemy)

if __name__ == "__main__":
    main()
