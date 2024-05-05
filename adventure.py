import sys
import json

class Game:
    def __init__(self, map_file):
        self.map_file = map_file
        self.current_room = None
        self.inventory = []

    def load_map(self):
        try:
            with open(self.map_file, 'r') as f:
                data = json.load(f)
                start_room = data["start"]
                rooms = data["rooms"]
                self.rooms = {room["name"]: room for room in rooms}
                if start_room not in self.rooms:
                    raise Exception("Start room not found")
                self.current_room = start_room
        except Exception as e:
            print("Invalid map format:", e, file=sys.stderr)
            sys.exit(1)

    def show_room(self):
        room = self.rooms[self.current_room]
        print("> " + room["name"])
        print(room["desc"])
        if "items" in room and room["items"]:
            print("Items:", ", ".join(room["items"]))
        print("Exits:", ", ".join(room["exits"]))
        if self.inventory:
            print("Inventory:", ", ".join(self.inventory))
        print("What would you like to do?")

    def execute_command(self, command):
        if command == "quit":
            print("Goodbye!")
            sys.exit(0)
        elif command == "look":
            self.show_room()
        elif command == "inventory":
            if not self.inventory:
                print("You're not carrying anything.")
            else:
                print("Inventory:")
                for item in self.inventory:
                    print(" ", item)
        elif command.startswith("go "):
            direction = command[3:]
            if direction in self.rooms[self.current_room]["exits"]:
                self.current_room = self.rooms[self.current_room]["exits"][direction]
                self.show_room()
            else:
                print("There's no way to go", direction + ".")
        elif command.startswith("get "):
            item = command[4:]
            if "items" in self.rooms[self.current_room] and item in self.rooms[self.current_room]["items"]:
                self.inventory.append(item)
                self.rooms[self.current_room]["items"].remove(item)
                print("You pick up the", item + ".")
            else:
                print("There's no", item, "anywhere.")
        else:
            print("Sorry, I didn't understand that command.")

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 adventure.py [map filename]", file=sys.stderr)
        sys.exit(1)

    game = Game(sys.argv[1])
    game.load_map()
    game.show_room()

    while True:
        command = input().strip().lower()
        game.execute_command(command)

if __name__ == "__main__":
    main()
