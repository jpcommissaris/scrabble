
class Player: 
    def __init__(self, _id):
        self.tiles = [] 
        self.score = 0 
        self.id = _id
        self.name = ''
        self.done = False
    
    def add_tiles(self, tile_bag):
        if(tile_bag and len(self.tiles) < 7):
            needed = 7 - len(self.tiles)
            amount = needed if needed < len(tile_bag)  else len(tile_bag)
            new_tiles= tile_bag[:amount]
            del tile_bag[:amount]
            self.tiles += new_tiles
    
    def remove_tiles(self, word): 
        for letter in word:
            remove_if_exists(self.tiles, letter)


def remove_if_exists(arr, element):
    try:
        arr.remove(element)
    except ValueError:
        pass



