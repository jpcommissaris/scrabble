import unittest
from game import Game
from board import Board
from player import Player

TILES = ['t', 'e', 's', 't', 'i', 'n', 'g']
TILE_BAG = ['a', 't', 'i', 'l', 'e', 's']*3
BOARD_TEST = [
    ['_','h','o','w'],
    ['_','_','_','_'],
    ['_','_','w','_'],
    ['a','_','e','_'],
]
BOARD_INIT = [
    ['_','_','_','_'],
    ['_','_','_','_'],
    ['_','_','_','_'],
    ['_','_','_','_'],
]

class TestGameInputValidation(unittest.TestCase): 

    def __init__(self, *args, **kwargs):
        super(TestGameInputValidation, self).__init__(*args, **kwargs)
        self.game = Game(size=4, players=2)
        self.player = self.game.players[0]
        self.player.tiles = TILES

    def run_validation_tests(self, message, tests):
    # helper method for the tests involving validating input
        self.game.board.board = BOARD_TEST
        for test_name, inputs in tests.items():
            print(test_name)
            self.assertEqual(message, self.game.check_if_valid(self.player, inputs)[1])
    

    def test_init(self):
        self.assertEqual(self.game.board.board, BOARD_INIT)
        self.assertEqual(len(self.game.tiles), 100-len(self.game.players)*7)
    

    def test_invalid_input(self):
        message = 'Invalid inputs!'
        tests = {'no_input': []}
        self.run_validation_tests(message, tests)

    def test_invalid_word(self):
        message = 'Invalid! This word does not exist'
        tests = {'not_a_word': ['ofksogkd', 1, 1, 'left']}
        self.run_validation_tests(message, tests)

    def test_invalid_board_space(self):
        message = 'Invalid! You are using space outside the board'
        tests = {
            'out-left': ['test', 0, -2, 'left'], 
            'out-right': ['set', 0, 2, 'left'],
            'out-top': ['test', -2, 0, 'down'], 
            'out-bottom': ['test', 2, 0, 'down'], 
        }
        self.run_validation_tests(message, tests)

    def test_invalid_use_of_tiles(self):
        message = 'Invalid! You used no tiles or tiles you dont have'
        tests = {'wrong-tiles': ['word', 1, 0, 'left'],}
        self.run_validation_tests(message, tests)  

    def test_invalid_tile_replacement(self):
        message = 'Invalid! You are trying to replace a tile on the board'
        tests = {
            'covering-vertical': ['set', 0, 0, 'left'], 
            'covering-horizontal': ['set', 0, 1, 'down'], 
        }
        self.run_validation_tests(message, tests)  
    def test_invalid_placement(self):
        message = 'Invalid! This word placement creates an illegal board'
        tests = {'adds-nonword': ['tin', 1, 1, 'down'],}
        self.run_validation_tests(message, tests)  
    
    def test_valid_moves(self):
        message = 'Nice Move!'
        tests = {
            'overlapping': ['ates', 3, 0, 'left'], 
            'on-edge': ['set', 0, 0, 'down'], 
        }
        self.run_validation_tests(message, tests)  


class TestGameStateUpdate(unittest.TestCase): 

    def __init__(self, *args, **kwargs):
        super(TestGameStateUpdate, self).__init__(*args, **kwargs)
        self.game = Game(size=4, players=2)

    # -- test that board state updates correctly with multiple players
    
    def test_skip(self):
        p0 = self.game.players[0]
        self.game.turn = 0
        self.game.tiles = ['n', 'e', 'w'] 
        _, message = self.game.do_skip(p0)
        self.assertEqual(message, 'You Passed!')
        self.assertEqual(p0.tiles[4:], ['n', 'e', 'w'] )
        self.assertEqual(self.game.turn, 1) 

    
    def test_valid_inputs(self):
        p1 = self.game.players[0]
        self.game.turn = 1
        p1.tiles = ['b', 'a', 'g']
        inputs = ['bag', 0, 0, 'down']
        is_true, _ = self.game.check_if_valid(p1, inputs)
        self.game.update_state(p1, inputs)
        self.assertEqual(is_true, True)
        self.assertEqual(self.game.turn, 0) 
        self.assertEqual(p1.score, 3) 
    
    def test_done(self):
        p0 = self.game.players[0]
        self.game.tiles = [] 
        _, message = self.game.do_skip(p0)
        self.assertEqual(message, 'Good game, your score is 0')



        
        


class TestPlayer(unittest.TestCase): 
    WORD = 'hey'
    def __init__(self, *args, **kwargs):
        super(TestPlayer, self).__init__(*args, **kwargs)
        self.player = Player(0)
    
    def test_remove_tiles(self):
        self.player.tiles = ['a','b','c','h','e','y','d']
        self.player.remove_tiles(TestPlayer.WORD)
        self.assertEqual(['a','b','c','d'], self.player.tiles)
        print('remove-tiles')
    
    def test_add_tiles(self):
        tile_bag = ['a', 'd', 'd']
        self.player.tiles = ['a','b','c','d']
        self.player.add_tiles(tile_bag)
        self.assertEqual(['a','b','c','d', 'a','d','d'], self.player.tiles)
        print('add-tiles')

    def test_add_last_tiles(self):
        tile_bag = ['a', 'd', 'd', 'l']
        self.player.tiles = ['a']
        self.player.add_tiles(tile_bag)
        self.assertEqual(['a','a','d','d','l'], self.player.tiles)
        self.player.add_tiles(tile_bag) # nothing in bag
        self.assertEqual(['a','a','d','d','l'], self.player.tiles)
        print('add-last-tiles')

class TestBoard(unittest.TestCase): 
    def test_get_words(self):
        board = Board(BOARD_TEST)
        self.assertEqual(board.get_words(), ['how', 'we'])



if __name__ == '__main__':
    unittest.main()


