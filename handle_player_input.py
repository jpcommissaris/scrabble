# -- handles player input for CLI -- 

def handle_player_input(player_input):
        inputs = player_input.split()
        if skip(inputs): 
            return '!skip'
        elif invalid(inputs): 
            return []
        return format_input(inputs)

def invalid(inputs):
    return not inputs or len(inputs) != 4  

def skip(inputs):
    return inputs and inputs[0] == '!skip' 

def format_input(inputs):
    word = inputs[0].lower()
    row = get_decimal(inputs[1])
    col = get_decimal(inputs[2])
    direction = get_direction(inputs[3])
    return (word, row, col, direction)

def get_decimal(hex):
    try: 
        num = int(f'0x{hex}', 16)
        return num-1 if 1 <= num <= 15 else 0
    except: 
        return 0

def get_direction(direction):
    lefts = ['left', 'LEFT', 'Left', 'horizontal', 'h', '>', 'l', 'L']
    return 'left' if direction in lefts else 'down'