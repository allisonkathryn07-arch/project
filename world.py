class Item:
    def __init__(self, name, item_type, value):
        self.name = name
        self.item_type = item_type  # "potion", "sword", "armor", "quest_item"
        self.value = value

class Map:
    def __init__(self):
        self.width = 10
        self.height = 10
        # Symbols: '.' = Empty, 'P' = Player, 'M' = Monster, 'B' = Boss, 'N' = NPC, 'I' = Item
        self.grid = [["." for _ in range(self.width)] for _ in range(self.height)]
        
        # Populate Items (5 total)
        self.items = {
            (1, 2): Item("Rusty Sword", "sword", 5),
            (3, 1): Item("Iron Shield", "armor", 3),
            (5, 5): Item("Health Potion", "potion", 20),
            (7, 2): Item("Mana Potion", "potion", 15),
            (2, 7): Item("Goblin Relic", "quest_item", 0)
        }
        
        # Populate Monsters (5 basic, 1 boss)
        self.monsters = {
            (2, 3): "Goblin Scamp",
            (4, 6): "Feral Wolf",
            (1, 6): "Zombie",
            (6, 2): "Skeleton",
            (8, 5): "Orc Scout"
        }
        self.boss_pos = (8, 8)
        self.npc_pos = (0, 2)
        
    def display(self, player_pos):
        import os
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=== TERMINAL WORLD MAP ===")
        for y in range(self.height):
            row_str = ""
            for x in range(self.width):
                if (x, y) == player_pos:
                    row_str += " P "
                elif (x, y) == self.npc_pos:
                    row_str += " N "
                elif (x, y) == self.boss_pos:
                    row_str += " B "
                elif (x, y) in self.monsters:
                    row_str += " M "
                elif (x, y) in self.items:
                    row_str += " I "
                else:
                    row_str += f" {self.grid[y][x]} "
            print(row_str)
        print("==========================")
        print("Legend: P=Player | N=NPC | M=Monster | B=Boss | I=Item")
