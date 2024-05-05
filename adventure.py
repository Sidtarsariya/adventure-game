def main():
    """
    The main entry point for the game.

    Loads the map file, validates it, and starts the game loop.
    """
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <map_file>")
        sys.exit(1)

    map_file = sys.argv[1]
    try:
        with open(map_file, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Map file '{map_file}' not found")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Map file '{map_file}' is invalid JSON")
        sys.exit(1)

    validation_error = validate_map(data)
    if validation_error:
        print(f"Error: Map validation failed: {validation_error}")
        sys.exit(1)

    # Initialize game state
    current_room = data["start"]
    player_inventory = []

    while True:
        # Get user input
        command = input("> ").lower().strip()

        # Handle commands
        if command == "quit":
            break
        elif command in ["north", "south", "east", "west"]:
            # Check for valid direction in current room exits
            if command not in current_room["exits"]:
                print(f"You can't go {command}.")
            else:
                current_room = data["rooms"][current_room["exits"][command]]
        elif command == "look":
            print(current_room["desc"])
        elif command == "get":
            # Check for item in current room and add to inventory
            if "items" not in current_room or len(current_room["items"]) == 0:
                print("There is nothing here to get.")
            else:
                item = current_room["items"][0]
                player_inventory.append(item)
                current_room["items"].remove(item)
                print(f"You picked up {item}.")
        elif command == "inventory":
            if not player_inventory:
                print("Your inventory is empty.")
            else:
                print("You are carrying:")
                for item in player_inventory:
                    print(f"- {item}")
        else:
            print(f"I don't understand '{command}'.")

    print("Thanks for playing!")

if __name__ == "__main__":
    main()
