import json
import sys


def validate_map(data):
    """
    Validates a map file against the expected schema.

    Args:
        data: The map data loaded from a JSON file.

    Returns:
        A string containing an error message if validation fails, None otherwise.
    """
    if "start" not in data or "rooms" not in data:
        return "Map is missing required fields: 'start' or 'rooms'"

    rooms = data["rooms"]
    for room in rooms:
        if "name" not in room or "desc" not in room or "exits" not in room:
            return (
                "Room is missing required fields: 'name', 'desc', or 'exits'"
            )
        if not isinstance(room["name"], str):
            return f"Room name '{room['name']}' is not a string"
        if not isinstance(room["desc"], str):
            return f"Room description '{room['desc']}' is not a string"
        if not isinstance(room["exits"], dict):
            return f"Room exits '{room['exits']}' is not a dictionary"
        for direction, exit_id in room["exits"].items():
            if not isinstance(direction, str):
                return f"Exit direction '{direction}' is not a string"
            if exit_id not in [room["name"] for room in rooms]:
                return f"Room '{room['name']}' exits to invalid room '{exit_id}'"
        if "items" in room and not isinstance(room["items"], list):
            return f"Room items '{room['items']}' is not a list"
        for item in room.get("items", []):
            if not isinstance(item, str):
                return f"Room item '{item}' is not a string"

    start_room = data["start"]
    if start_room not in [room["name"] for room in rooms]:
        return f"Start room '{start_room}' does not exist"

    return None


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

    # Implement the game loop, including handling user input, parsing commands,
    # updating the game state, and printing output
    # ...


if __name__ == "__main__":
    main()
