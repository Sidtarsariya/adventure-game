import json
import sys

class Game:
    def __init__(self, map_file):
        with open(map_file, 'r') as f:
            self.map = json.load(f)
        self.current_room = self.map['start']
        self.inventory = []

    def print_room(self):
        room = self.get_room(self.current_room)
        print(f"> {room['name']}")
        print(room['desc'])
        print("Exits:", ', '.join(room['exits'].keys()))
        if room.get('items'):
            print("Items:", ', '.join(room['items']))

    def get_room(self, room_name):
        for room in self.map['rooms']:
            if room['name'] == room_name:
                return room
        return None

    def go(self, direction):
        room = self.get_room(self.current_room)
        if direction in room['exits']:
            self.current_room = room['exits'][direction]
            self.print_room()
        else:
            print("There's no way to go", direction)

    def get(self, item):
        room = self.get_room(self.current_room)
        if item in room.get('items', []):
            self.inventory.append(item)
            room['items'].remove(item)
            print(f"You pick up the {item}.")
        else:
            print(f"There's no {item} anywhere.")

    def inventory(self):
        if not self.inventory:
            print("You're not carrying anything.")
        else:
            print("Inventory:")
            for item in self.inventory:
                print(f"  {item}")

    def quit(self):
        print("Goodbye!")
        sys.exit(0)

    def play(self):
        while True:
            self.print_room()
            command = input("What would you like to do? ").lower()
            if command.startswith('go '):
                self.go(command[3:])
            elif command.startswith('get '):
                self.get(command[4:])
            elif command == 'look':
                self.print_room()
            elif command == 'inventory':
                self.inventory()
            elif command == 'quit':
                self.quit()
            else:
                print("Sorry, I didn't understand that.")

if __name__ == '__main__':
    if len(sys.argv)!= 2:
        print("Usage: python3 adventure.py <map_file>")
        sys.exit(1)
    game = Game(sys.argv[1])
    game.play()