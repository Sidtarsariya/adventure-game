import sys
import json
import difflib

class TextAdventure:
    def __init__(self, map_file):
        self.load_map(map_file)
        self.current_room = self.map_data["start"]
        self.inventory = []

    def load_map(self, map_file):
        with open(map_file, "r") as f:
            self.map_data = json.load(f)

    def play(self):
        self.print_room_description()
        while True:
            command = input("What would you like to do? ").strip().lower()
            if command in ["quit", "exit"]:
                print("Goodbye!")
                break
            self.process_command(command)

    def print_room_description(self):
        # Find the index of the current room based on its name
        current_room_index = None
        for i, room in enumerate(self.map_data["rooms"]):
            if room["name"] == self.current_room:
                current_room_index = i
                break

        if current_room_index is not None:
            # Access the room information using the integer index
            room_info = self.map_data["rooms"][current_room_index]
            # Print the room description
            print("> " + room_info["name"] + "\n")
            print(room_info["desc"] + "\n")
            # Print exits
            exits = room_info["exits"]
            print("Exits: " + ", ".join(exits.keys()) + "\n")
            print("What would you like to do? ", end="")
        else:
            print("Error: Current room not found in map data.")


    def print_exits(self, room_info):
        exits = ", ".join(room_info["exits"].keys())
        print(f"Exits: {exits}\n")

    def print_inventory(self):
        if self.inventory:
            print("Inventory:")
            for item in self.inventory:
                print(f"  {item}")
        else:
            print("You're not carrying anything.\n")

    def process_command(self, command):
        if command.startswith("go "):
            direction = command.split(" ", 1)[1]
            self.go(direction)
        elif command.startswith("get "):
            item = command.split(" ", 1)[1]
            self.get_item(item)
        elif command.startswith("drop "):
            item = command.split(" ", 1)[1]
            self.drop_item(item)
        elif command == "look":
            self.print_room_description()
        elif command == "inventory":
            self.print_inventory()
        elif command == "help":
            self.print_help()
        else:
            self.process_abbreviated_command(command)

    def process_abbreviated_command(self, command):
        all_commands = ["go", "get", "drop", "look", "inventory", "quit", "exit", "help"]
        matches = difflib.get_close_matches(command, all_commands)
        if len(matches) == 1:
            self.process_command(matches[0])
        elif len(matches) > 1:
            print(f"Did you mean {' or '.join(matches)}?\n")
        else:
            print("Sorry, I don't understand that command.\n")

    def go(self, direction):
        room_info = self.map_data["rooms"][self.current_room]
        exits = room_info["exits"]
        if direction in exits:
            self.current_room = exits[direction]
            self.print_room_description()
        else:
            print(f"There's no way to go {direction}.\n")

    def get_item(self, item):
        room_info = self.map_data["rooms"][self.current_room]
        if "items" in room_info and item in room_info["items"]:
            self.inventory.append(item)
            room_info["items"].remove(item)
            print(f"You pick up the {item}.\n")
        else:
            print(f"There's no {item} here.\n")

    def drop_item(self, item):
        if item in self.inventory:
            self.inventory.remove(item)
            room_info = self.map_data["rooms"][self.current_room]
            if "items" in room_info:
                room_info["items"].append(item)
            else:
                room_info["items"] = [item]
            print(f"You drop the {item}.\n")
        else:
            print(f"You're not carrying {item}.\n")

    def print_help(self):
        all_commands = ["go [direction]", "get [item]", "drop [item]", "look", "inventory", "quit", "help"]
        print("You can run the following commands:")
        for cmd in all_commands:
            print(f"  {cmd}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 adventure.py [map filename]")
        sys.exit(1)

    map_file = sys.argv[1]
    game = TextAdventure(map_file)
    game.play()
