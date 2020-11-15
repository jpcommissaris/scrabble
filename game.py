import copy
import random
from board import Board
from player import Player
from words import Words

class Game:
    """
    Holds game state and updates when given input
    """
    WORDS = Words('wordlist.json')

    def __init__(self, players=2, size=15):
        self.turn = 0
        self.size = size
        self.players = [Player(i) for i in range(players)]
        self.board = Board([['_'] * size for _ in range(size)])
        self.tiles = self.generate_tile_bag()
        for p in self.players: 
            p.add_tiles(self.tiles)
    
    def generate_tile_bag(self):
        letters = list('abcdeefghijklmnopqrstuvwxyz')
        count =   list('922493232911427921646422121')
        count = [int(i) for i in count]
        tile_bag = []
        for letter, count in zip(letters, count):
            tile_bag += [letter] * count
        random.shuffle(tile_bag)
        return tile_bag

    # -- update game state -- 
    def update_state(self, player, inputs):
        if(inputs == '!skip'):
            return self.do_skip(player)     
        return self.do_move(player, inputs)
    
    def do_skip(self, player): 
        if(len(self.tiles) == 0):
            player.done = True
            message = f'Good game, your score is {player.score}'
        else:
            player.tiles = player.tiles[3:]
            player.add_tiles(self.tiles)
            message = 'You Passed!'
        self.swap_turns()
        return True, message
    
    def do_move(self, player, inputs):
        valid, message = self.check_if_valid(player, inputs)
        if valid:
            word = inputs[0]
            self.update_board(inputs)
            self.update_score(player, word)
            self.update_tiles(player, word)
            self.swap_turns()
        return valid, message

    def update_board(self, inputs):
        self.board.add_inputs(inputs)

    def update_score(self, player, word):
        player.score += len(word)
    
    def update_tiles(self, player, word):
        player.remove_tiles(word)
        player.add_tiles(self.tiles)

    def swap_turns(self):
        self.turn = self.turn+1 if self.turn < len(self.players)-1 else 0 

    def game_over(self):
        for player in self.players:
            if(not player.done):
                return False
        return True
    
    # -- check for valid input -- 
    def check_if_valid(self, player, inputs):
        if not inputs or len(inputs) != 4:
            return False, 'Invalid inputs!'
        word = inputs[0]
        if not self.word_exists(word):
            return False, 'Invalid! This word does not exist'
        elif self.out_of_bounds(inputs):
            return False, 'Invalid! You are using space outside the board'
        elif not self.player_has_tiles_for_word(player.tiles, inputs):
            return False, 'Invalid! You used no tiles or tiles you dont have'
        elif self.letter_on_taken_tile(inputs):
            return False, 'Invalid! You are trying to replace a tile on the board'
        elif self.invalid_placement(inputs):
            return False, 'Invalid! This word placement creates an illegal board'
        return True, 'Nice Move!'

    def word_exists(self, word):
        return Game.WORDS.contains(word)

    def out_of_bounds(self, inputs):
        word, row, col, direction = inputs
        if(not (0 <= row < self.size and  0 <= col < self.size)):
            return True
        elif(direction =='left'):
            return col + len(word) > self.size 
        else:
            return row + len(word) > self.size 
    
    def player_has_tiles_for_word(self, tiles, inputs):
        word = inputs[0]
        tmp_tiles = copy.deepcopy(tiles)
        tiles_used = 0
        for index, letter in enumerate(word):
            if self.__tile_has_letter_value(letter, index, inputs[1:]):
                continue
            elif letter not in tmp_tiles:
                return False
            tiles_used+=1
            remove_if_exists(tmp_tiles, letter)     
        return True if tiles_used > 0 else False
    
    def __tile_has_letter_value(self, letter, index, some_inputs):
        row, col, direction = some_inputs
        if(direction =='left'):
            return self.board.get(row, col+index) == letter
        return self.board.get(row+index, col) == letter
    
    def letter_on_taken_tile(self, inputs):
        word, row, col, direction = inputs
        for i, letter in enumerate(word):
            if(direction=='left' and self.__check_for_overlap(letter, row, col+i)):
                return True 
            elif(direction !='left' and self.__check_for_overlap(letter, row+i, col)):
                return True
        return False

    def __check_for_overlap(self, letter, row, col):
        current_tile = self.board.get(row, col)
        if(current_tile == '_' or current_tile == letter):
            return False
        return True

    def invalid_placement(self, inputs):
        tmp_board = copy.deepcopy(self.board)
        tmp_board.add_inputs(inputs)
        words = tmp_board.get_words()
        for word in words:
            if(not self.word_exists(word)):
                return True
        return False


# -- helper funcs --     
def remove_if_exists(arr, element):
    try:
        arr.remove(element)
    except ValueError:
        pass



