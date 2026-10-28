from world import Map
from entities import Player
from game import GameEngine

def main():
    player = Player()
    world_map = Map()
    engine = GameEngine(player, world_map)

    print("Welcome to Terminal RPG!")
    print("Controls: W (Up), A (Left), S (Down), D (Right), I (Inventory), Q (Quit)")
    input("Press Enter to begin your adventure...")

    while engine.running:
        engine.world_map.display((player.x, player.y))
        print(f"Stats -> HP: {player.hp}/{player.max_hp} | Location: ({player.x}, {player.y}) | Quest: {player.quest_status}")
        
        cmd = input("Command (W/A/S/D or I for Inventory): ").lower().strip()
        
        if cmd == 'q':
            print("Thanks for playing!")
            break
        elif cmd == 'i':
            print("\n--- Current Inventory ---")
            if not player.inventory:
                print("[Empty]")
            for item in player.inventory:
                print(f"- {item.name} ({item.item_type.capitalize()})")
            input("\nPress Enter to close inventory...")
        elif cmd in ['w', 'a', 's', 'd']:
            engine.move_player(cmd)

if __name__ == "__main__":
    main()
