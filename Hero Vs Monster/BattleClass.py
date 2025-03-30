import random
import time

class Battle:  # Capitalized class name as per convention

    def battleStart(self, Player, Enemy):
        dayIsSaved = False

        print(f"{Player.name} encounters a {Enemy.name}!")
        print(f"{Player.name} Health: {Player.health}, Armor: {Player.armor}")
        print(f"{Enemy.name} Health: {Enemy.health}, Armor: {Enemy.armor}\n")

        while Player.is_alive() and not dayIsSaved:
            Player.rollInitiative()
            Enemy.rollInitiative()

            if Player.initiative >= Enemy.initiative:
                print(f"{Player.name} attacks first!")
                if self.hitCheckPlayer(Player, Enemy):
                    self.playerAttack(Player, Enemy)

                if Enemy.isDefeated:
                    Player.gain_exp(Enemy.experience)
                    break

                if self.hitCheckEnemy(Player, Enemy):
                    self.enemyAttack(Player, Enemy)

                if not Player.is_alive():
                    break
            else:
                print(f"{Enemy.name} attacks first!")
                if self.hitCheckEnemy(Player, Enemy):
                    self.enemyAttack(Player, Enemy)

                if not Player.is_alive():
                    break

                if self.hitCheckPlayer(Player, Enemy):
                    self.playerAttack(Player, Enemy)

                if Enemy.isDefeated:
                    Player.gain_exp(Enemy.experience)
                    break

            if random.randint(1, 20) == 20:
                print(f"{Player.name} has saved the day!")
                dayIsSaved = True
                break

            print(f"{Player.name} Health: {Player.health}")
            time.sleep(1)

    def hitCheckPlayer(self, Player, Enemy):
        if Player.aimAttack() >= Enemy.armor:
            print(f"{Player.name} hits the {Enemy.name}!")
            return True
        else:
            print(f"{Player.name} misses the {Enemy.name}!")
            return False

    def hitCheckEnemy(self, Player, Enemy):
        if Enemy.aimAttack() >= Player.armor:
            print(f"{Enemy.name} hits {Player.name}!")
            return True
        else:
            print(f"{Enemy.name} misses {Player.name}!")
            return False

    def playerAttack(self, Player, Enemy):
        damage = Player.attack()
        print(f"{Player.name} attacks the {Enemy.name} for {damage} damage!")
        Enemy.damaged(damage)

    def enemyAttack(self, Player, Enemy):
        damage = Enemy.attack()
        print(f"{Enemy.name} attacks {Player.name} for {damage} damage!")
        Player.damaged(damage)
