import json
import sys

def load_map(map_filename):
    try:
        with open(map_filename, 'r') as map_file:
            return json.load(map_file)
    except FileNotFoundError:
        print("Map file not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print("Invalid JSON format in map file.")
        sys.exit(1)

def validate_map(map_data):
    # Validate map structure according to the specifications
    if not isinstance(map_data, dict):
        print("Invalid map format: Map must be a JSON object.")
        sys.exit(1)

    if "start" not in map_data or "rooms" not in map_data:
        print("Invalid map format: Map must contain 'start' and 'rooms' keys.")
        sys.exit(1)

    start_room = map_data["start"]
    rooms = map_data["rooms"]

    if not isinstance(start_room, str):
        print("Invalid map format: 'start' must be a string.")
        sys.exit(1)

    if not isinstance(rooms, list):
        print("Invalid map format: 'rooms' must be a list.")
        sys.exit(1)

    room_names = set()
    for room in rooms:
        if not isinstance(room, dict) or "name" not in room or "desc" not in room or "exits" not in room:
            print("Invalid room format: Each room must have 'name', 'desc', and 'exits' keys.")
            sys.exit(1)

        room_name = room["name"]
        if not isinstance(room_name, str):
            print("Invalid room format: Room name must be a string.")
            sys.exit(1)

        if room_name in room_names:
            print("Invalid room format: Room names must be unique.")
            sys.exit(1)
        room_names.add(room_name)

        if not isinstance(room["desc"], str):
            print("Invalid room format: Room description must be a string.")
            sys.exit(1)

        exits = room["exits"]
        if not isinstance(exits, dict):
            print("Invalid room format: Exits must be a dictionary.")
            sys.exit(1)

        for direction, destination in exits.items():
            if not isinstance(direction, str) or not isinstance(destination, str):
                print("Invalid room format: Exit directions and destinations must be strings.")
                sys.exit(1)
            if destination not in room_names:
                print(f"Invalid room format: Exit destination '{destination}' does not exist.")
                sys.exit(1)

    print("Map validated successfully.")

# Now call validate_map in the main function after loading the map


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 adventure.py [map_filename]")
        sys.exit(1)

    map_filename = sys.argv[1]
    map_data = load_map(map_filename)
    validate_map(map_data)

    current_room = map_data["start"]
    rooms = {room["name"]: room for room in map_data["rooms"]}
    inventory = []

    verbs = {
        "go": "go",
        "look": "look",
        "get": "get",
        "inventory": "inventory",
        "quit": "quit",
        "help": "help"
    }

    while True:
        room = rooms[current_room]
        print(f"> {room['name']}\n\n{room['desc']}\n")
        print("Exits:", ", ".join(room["exits"]))
        print("Inventory:", ", ".join(inventory) if inventory else "Empty")
        command = input("\nWhat would you like to do? ").strip().lower()

        # Abbreviations handling
        command_parts = command.split()
        verb = command_parts[0]
        if verb in verbs:
            verb = verbs[verb]
        else:
            print("Invalid command. Type 'help' to see valid commands.")
            continue

        if verb == "go":
            direction = " ".join(command_parts[1:])
            if direction in room["exits"]:
                current_room = room["exits"][direction]
            else:
                print("There's no way to go", direction + ".")
        elif verb == "look":
            print(f"\n> {room['name']}\n\n{room['desc']}\n")
        elif verb == "get":
            item = " ".join(command_parts[1:])
            if item in room.get("items", []):
                inventory.append(item)
                room["items"].remove(item)
                print(f"You pick up the {item}.")
            else:
                print(f"There's no {item} anywhere.")
        elif verb == "drop":
            item = " ".join(command_parts[1:])
            if item in inventory:
                inventory.remove(item)
                room["items"].append(item)
                print(f"You drop the {item}.")
            else:
                print(f"You're not carrying {item}.")
        elif verb == "inventory":
            print("\nInventory:", ", ".join(inventory) if inventory else "Empty")
        elif verb == "quit":
            print("Goodbye!")
            sys.exit()
        elif verb == "help":
            print("\nYou can run the following commands:")
            print("  " + ", ".join(verbs.keys()))
            print("\nYou can also use exit directions as verbs.")
        else:
            print("Sorry, I don't understand that command.")

if __name__ == "__main__":
    main()


    # Game loop
    # Implement the game loop to handle player input and execute commands