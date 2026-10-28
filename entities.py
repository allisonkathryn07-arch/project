class Player:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.hp = 100
        self.max_hp = 100
        self.base_atk = 10
        self.base_def = 2
        self.inventory = []
        self.equipped_weapon = None
        self.equipped_armor = None
        self.quest_status = "Not Started" # "Not Started", "Active", "Completed"

    def get_atk(self):
        bonus = self.equipped_weapon.value if self.equipped_weapon else 0
        return self.base_atk + bonus

    def get_def(self):
        bonus = self.equipped_armor.value if self.equipped_armor else 0
        return self.base_def + bonus

class Enemy:
    def __init__(self, name, hp, atk, is_boss=False):
        self.name = name
        self.hp = hp
        self.atk = atk
        self.is_boss = is_boss

class NPC:
    def __init__(self):
        self.name = "Elder Thomas"
        self.dialogue_prompt = "Greetings Traveler. The Orcs stole our Goblin Relic. Bring it back to me! (Accept quest? y/n): "
        
    def interact(self, player):
        if player.quest_status == "Not Started":
            choice = input(self.dialogue_prompt).lower()
            if choice == 'y':
                player.quest_status = "Active"
                print(f"{self.name}: Thank you! Find the Relic ('I') at coordinates (2,7).")
            else:
                print(f"{self.name}: Please reconsider. The valley is in danger.")
        elif player.quest_status == "Active":
            # Check if player has the specific item
            has_relic = any(item.item_type == "quest_item" for item in player.inventory)
            if has_relic:
                player.quest_status = "Completed"
                # Remove relic from inventory
                player.inventory = [i for i in player.inventory if i.item_type != "quest_item"]
                print(f"\n{self.name}: You found it! Thank you! The path to the Dragon Boss at (8,8) is clear.")
                print("Your health has been completely restored as a reward!")
                player.hp = player.max_hp
            else:
                print(f"{self.name}: You haven't found the Goblin Relic yet. Keep searching!")
        else:
            print(f"{self.name}: Thank you again for saving our relic. Go defeat the Boss!")
