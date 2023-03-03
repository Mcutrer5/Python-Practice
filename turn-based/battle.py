import random 
import math
class Battle:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
    
    def fight(self):
        attacker = self.player1
        defender = self.player2
        # total defense for defender armor pieces
        total_defense = defender.defense
        crit_chance = random.randint(1, 30)
        
        if (crit_chance == 1):
            damage = (attacker.weapon.damage - math.floor(total_defense * (random.randint(2,5) / 10))) * 2
            print(f"{attacker.name} CRITICALLY STRIKES {defender.name} for {damage} damage!")
        else:
            damage = attacker.weapon.damage - math.floor(total_defense * (random.randint(2,5) / 10))
            print(f"{attacker.name} attacks {defender.name} for {damage} damage!\n{defender.name} had {total_defense} defense!")
        
        print("damage: ", damage)
        
        if damage < 0:
            damage = 0
        # subtract damage from defender hp
        defender.hp -= damage

        
        
        if defender.hp <= 0:
            if not defender.get_alive_status():
                print(f"{defender.name} has been defeated!")
            return

        print(f"{defender.name} has {defender.hp} HP left!")
