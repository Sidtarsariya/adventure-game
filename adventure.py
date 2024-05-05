import json
import sys

class Game:
    def __init__(self, map_filename):
        self.load_map(map_filename)
        self.current_room = self.map_data["start"]
        self.inventory = []

    def load_map(self, map_filename):
        try:
            with open(map_filename, 'r') as file:
                self.map_data = json.load(file)
        except FileNotFoundError:
            print(f"Error: Map file '{map_filename}' not found.")
            sys.exit(1)
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON format in map file '{map_filename}'.")
            sys.exit(1)

    def get_room_info(self, room_id):
        room_info = self.map_data["rooms"][room_id]
        description = room_info["desc"]
        exits = ", ".join(room_info["exits"].keys())
        items = ", ".join(room_info.get("items", []))
        return f"{description}\n\nExits: {exits}\nItems: {items}"

    def execute_command(self, command):
        command_parts = command.split()
        verb = command_parts[0].lower()

        if verb == "go":
            direction = command_parts[1].lower()
            exits = self.map_data["rooms"][self.current_room]["exits"]
            if direction in exits:
                self.current_room = exits[direction]
                return self.get_room_info(self.current_room)
            else:
                return "There's no way to go in that direction."

        elif verb == "look":
            return self.get_room_info(self.current_room)

        elif verb == "get":
            item = " ".join(command_parts[1:])
            room_items = self.map_data["rooms"][self.current_room].get("items", [])
            if item in room_items:
                self.inventory.append(item)
                room_items.remove(item)
                return f"You pick up the {item}."
            else:
                return f"There's no {item} here."

        elif verb == "inventory":
            if self.inventory:
                return "Inventory:\n  " + "\n  ".join(self.inventory)
            else:
                return "You're not carrying anything."

        elif verb == "quit":
            return "Goodbye!"

        else:
            return "Sorry, I don't understand that command."

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 adventure.py [map filename]")
        sys.exit(1)

    game = Game(sys.argv[1])
    print(game.get_room_info(game.current_room))

    while True:
        command = input("\nWhat would you like to do? ").strip()
        if not command:
            continue
        result = game.execute_command(command)
        print(result)
        if result == "Goodbye!":
            break

if __name__ == "__main__":
    main()
