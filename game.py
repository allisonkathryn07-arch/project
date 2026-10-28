import random
from entities import Enemy, NPC

class GameEngine:
    def __init__(self, player, world_map):
        self.player = player
        self.world_map = world_map
        self.npc = NPC()
        self.running = True

    def move_player(self, direction):
        dx, dy = 0, 0
        if direction == 'w': dy = -1
        elif direction == 's': dy = 1
        elif direction == 'a': dx = -1
        elif direction == 'd': dx = 1
        else:
            print("Invalid command! Use W/A/S/D to move.")
            return

        new_x = self.player.x + dx
        new_y = self.player.y + dy

        if 0 <= new_x < self.world_map.width and 0 <= new_y < self.world_map.height:
            self.player.x = new_x
            self.player.y = new_y
            self.check_tile_triggers()
        else:
            print("You hit a solid wall!")

    def check_tile_triggers(self):
        pos = (self.player.x, self.player.y)

        # 1. Trigger NPC Interaction
        if pos == self.world_map.npc_pos:
            self.npc.interact(self.player)
            input("\nPress Enter to continue...")

        # 2. Trigger Item Collection
        elif pos in self.world_map.items:
            item = self.world_map.items[pos]
            self.player.inventory.append(item)
            print(f"\nYou picked up: {item.name} ({item.item_type})!")
            del self.world_map.items[pos]
            
            # Auto-equip logic if it's equipment
            if item.item_type == "sword":
                self.player.equipped_weapon = item
                print(f"Equipped {item.name} (+{item.value} Attack)!")
            elif item.item_type == "armor":
                self.player.equipped_armor = item
                print(f"Equipped {item.name} (+{item.value} Defense)!")
            input("\nPress Enter to continue...")

        # 3. Trigger Normal Combat
        elif pos in self.world_map.monsters:
            monster_name = self.world_map.monsters[pos]
            enemy = Enemy(monster_name, hp=30, atk=8)
            self.battle(enemy)
            if self.player.hp > 0:
                del self.world_map.monsters[pos]
            input("\nPress Enter to continue...")

        # 4. Trigger Boss Combat
        elif pos == self.world_map.boss_pos:
            if self.player.quest_status != "Completed":
                print("\nA magical barrier blocks your path! Complete the Elder's quest first.")
                self.player.x, self.player.y = 7, 8  # Bounce player back
            else:
                boss = Enemy("Shadow Dragon (BOSS)", hp=120, atk=18, is_boss=True)
                self.battle(boss)
            input("\nPress Enter to continue...")

    def battle(self, enemy):
        print(f"\nA wild {enemy.name} blocks your way!")
        while enemy.hp > 0 and self.player.hp > 0:
            print(f"\nPlayer HP: {self.player.hp}/{self.player.max_hp} | {enemy.name} HP: {enemy.hp}")
            print("1. Attack")
            print("2. Drink Potion")
            choice = input("Choose action: ")

            if choice == "1":
                dmg_to_enemy = max(1, self.player.get_atk() - random.randint(0, 3))
                enemy.hp -= dmg_to_enemy
                print(f"You strike the {enemy.name} for {dmg_to_enemy} damage!")
            elif choice == "2":
                potions = [i for i in self.player.inventory if i.item_type == "potion"]
                if potions:
                    used_pot = potions[0]
                    self.player.hp = min(self.player.max_hp, self.player.hp + used_pot.value)
                    self.player.inventory.remove(used_pot)
                    print(f"You drank {used_pot.name} and healed {used_pot.value} HP!")
                else:
                    print("You have no potions!")
                    continue
            else:
                print("Invalid choice, you fumbled your turn!")

            if enemy.hp > 0:
                dmg_to_player = max(1, enemy.atk - self.player.get_def())
                self.player.hp -= dmg_to_player
                print(f"{enemy.name} counterattacks doing {dmg_to_player} damage!")

        if self.player.hp <= 0:
            print("\nYou were slain in battle... GAME OVER.")
            self.running = False
        elif enemy.hp <= 0:
            print(f"\nYou defeated the {enemy.name}!")
            if enemy.is_boss:
                print("\nCongratulations! You have slain the Shadow Dragon and won the game!")
                self.running = False
