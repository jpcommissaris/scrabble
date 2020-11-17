from handle_player_input import handle_player_input
from game import Game


DIGITS = '1 2 3 4 5 6 7 8 9 a b c d e f'
SIZE = 15 
PLAYERS = 2

class Scrabble_CLI: 
    """
    Runs an instance of game and handles i/o via the CLI
    """

    def __init__(self):
        self.game = Game(players=PLAYERS, size=15)

    def run(self):
        print('Welcome to Scrabble')
        self.ask_names()
        while not self.game.game_over():
            self.do_turns()
        print('Game over')
        self.print_scores()
    
    def ask_names(self):
        for p in self.game.players: 
            p.name = input(f'Player {p.id} enter your name! ')
    
    def do_turns(self):
        for player in self.game.players:
            if not player.done:
                self.print_game(player)
                self.cycle_input_until_valid(player)

    def print_game(self, player):
        self.print_board()
        self.print_scores()
        self.print_tiles(player)

    def print_board(self): 
        board = self.game.board.to_array()  
        print('____________ Board Start ____________\n')
        print(f'     {DIGITS}')
        for i, row in enumerate(board):
            print(f'   {DIGITS[i*2]}', end='')
            for tile in row:  
                print(f'|{tile}', end='')
            print('|')
        print('')
    
    def print_scores(self):
        scores = [f'{player.name}: {player.score}pts ' for player in self.game.players]
        print(f'Scores: {"".join(scores)}')
    
    def print_tiles(self, player):
        tiles = [f'{tile} ' for tile in player.tiles]
        print(f'Tiles in bag: {len(self.game.tiles)}')
        print(f'Tiles: {"".join(tiles)}')
       

    def cycle_input_until_valid(self, player):
        valid, args = False, False 
        while not valid: 
            args = self.get_input_if_exists(player)
            valid, message = self.game.update_state(player, args)
            print(message)
    
    def get_input_if_exists(self, p):
        name = p.name if p.name else p.id
        player_input = input(f'{name}, enter a word "$ word row col direction [left/down]" or "$ !skip" \n$ ')
        return handle_player_input(player_input)
            
        

        







