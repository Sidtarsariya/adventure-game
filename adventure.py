import json
import sys

# Load and validate map file
with open(sys.argv[1], 'r') as f:
    map_data = json.load(f)

# Define initial game state
player_location = 0
player_inventory = []

# Main game loop
while True:
    # Display current room information
    current_room = map_data[player_location]
    print(f'> {current_room["name"]}\n\n{current_room["desc"]}\n\nExits: {", ".join(current_room["exits"])}')

    # Get user input
    user_input = input("What would you like to do? ")

    # Parse user input and execute appropriate verb
    if user_input.lower() in ['quit', 'exit']:
        # Exit game cleanly
        print('Goodbye!')
        break
    elif user_input.lower() == 'look':
        # Show current room information again
        print(f'> {current_room["name"]}\n\n{current_room["desc"]}\n\nExits: {", ".join(current_room["exits"])}')
    elif user_input.lower().startswith('go '):
        # Try to move in specified direction
        direction = user_input[3:].strip()
        if direction in current_room['exits']:
            player_location = current_room['exits'][direction]
            current_room = map_data[player_location]
            print(f'You go {direction}.\n\n> {current_room["name"]}\n\n{current_room["desc"]}\n\nExits: {", ".join(current_room["exits"])}')
        else:
            print(f"There's no way to go {direction}.")
    elif user_input.lower().startswith('get '):
        # Pick up specified item if it exists in current room
        item_name = user_input[4:].strip()
        if item_name in current_room.get('items', []):
            player_inventory.append(item_name)
            current_room['items'].remove(item_name)
            print(f'You pick up the {item_name}.\n')
        else:
            print(f"There's no {item_name} anywhere.")
    elif user_input.lower() == 'inventory':
        # Display player inventory
        if player_inventory:
            print('Inventory:')
            for item in player_inventory:
                print(f'  {item}')
        else:
            print("You're not carrying anything.")
    else:
        # Unknown command
        print("I don't understand what you mean.")