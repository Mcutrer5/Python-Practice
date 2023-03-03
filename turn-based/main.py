import player
import battle
import time

STARTING_ARMOR = {
        "head": "Leather Helmet",
        "body": "Leather Armor",
        "legs": "Leather Pants",
        "feet": "Leather Boots"
    }

def get_name():
    name = input("What is your name? ")
    return name

def set_player(name):
    player1 = player.Player(name, 100, 1)
    armor = player.Armor()
    weapon = player.Weapon()
    
    armor.set_multiple(STARTING_ARMOR)
    player1.armor = armor
    
    weapon.set_equipped("sword", "Steel Sword", 20, 1)
    player1.weapon = weapon
    return player1

def set_enemy():
    enemy = player.Player("Enemy", 100, 1)
    armor = player.Armor()
    weapon = player.Weapon()
    
    armor.set_multiple(STARTING_ARMOR)
    enemy.armor = armor
    
    weapon.set_equipped("sword", "Steel Sword", 20, 1)
    enemy.weapon = weapon
    return enemy

def check_alive(player, enemy):
    if player.get_alive_status() == False:
        print("You died!")
        exit()
    elif enemy.get_alive_status() == False:
        print("You win!")
        exit()

def game():
    name = get_name()
    player = set_player(name)
    enemy = set_enemy()
    
    while (player.get_alive_status() == True and enemy.get_alive_status() == True):
        player_attack = battle.Battle(player, enemy)
        enemy_attack = battle.Battle(enemy, player)
    
        choice = input("What do you want to do?\n[attack, defend, run] > ")
        match choice:
            case "attack":
                player_attack.fight()
            case "defend":
                continue
            case "run":
                continue
            case _:
                print("Invalid choice")
                continue
            
        check_alive(player, enemy)
        
        # wait for 2 seconds 
        time.sleep(2)
        enemy_attack.fight()
        check_alive(player, enemy)
        
def main():
    game()
    

if __name__ == "__main__":
    main()