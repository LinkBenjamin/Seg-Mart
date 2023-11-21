identity = 'nobody'
currentzone = ''
object_interaction = ''
current_coordinates = (0,0)
shopping_bag = []

# Data stored here to map tiles, images, and such
# Fields:
#  - number (code used in map objects)
#  - filename (in /static/objects, all .png)
#  - hitbox adjustment (% shrink / stretch for hitbox sizing)
#  - item type (ground, object, decoration)
#  - Item Name (pretty print)
game_items = {
    'a': ['floor_tile', 0, 'ground', 'Tile Floor'],
    'b': ['wall_brick', 0, 'ground', 'Brick Wall'],
    'c': ['door', 0, 'ground', 'Door'],
    'd': ['grass_1', 0, 'ground', 'Grass'],
    'e': ['grass_2', 0, 'ground', 'Grass'],
    'f': ['floor_plain', 0, 'ground', 'Floor'],
    'g': ['roof_left', 0, 'ground', 'Roof'],
    'h': ['roof_center', 0, 'ground', 'Roof'],
    'i': ['roof_right', 0, 'ground', 'Roof'],
    'j': ['path_v', 0, 'ground', 'Path'],
    'k': ['table_h_left', 0, 'decoration', 'Table'],
    'l': ['table_h_center', 0, 'decoration', 'Table'],
    'm': ['table_h_right', 0, 'decoration', 'Table'],
    'n': ['table_v_top', 0, 'decoration', 'Table'],
    'o': ['motor_oil', 20, 'object', 'Motor Oil'],
    'p': ['plant', 20, 'object', 'Plant'],
    'q': ['laptop', 20, 'object', 'Laptop'],
    'r': ['drink', 20, 'object', 'Drink'],
    's': ['table_v_bottom', 0, 'decoration', 'Table'],
    't': ['kiosk', 20, 'object', 'Kiosk'],
    'u': ['path_h', 0, 'ground', 'Path'],
    'v': ['shoes', 20, 'object', 'Shoes'],
    'w': ['table_v_center', 0, 'decoration', 'Table']
}