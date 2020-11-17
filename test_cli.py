import unittest
from unittest import mock
from scrabble_cli import Scrabble_CLI
from handle_player_input import handle_player_input


class TestCLI(unittest.TestCase): 

    def __init__(self, *args, **kwargs):
        super(TestCLI, self).__init__(*args, **kwargs)
        self.cli = Scrabble_CLI()

    def test_ask_name(self):
        with mock.patch('builtins.input', side_effect=['Julian', 'Paul']):
            self.cli.ask_names()
            self.assertEqual(self.cli.game.players[0].name, 'Julian')
            self.assertEqual(self.cli.game.players[1].name, 'Paul')

    def test_valid_input(self):
        self.cli.game.players[0].tiles += ['a', 't']
        with mock.patch('builtins.input', return_value='at 1 2 left'):
            self.cli.cycle_input_until_valid(self.cli.game.players[0])

    def test_handling_input(self):
        tests = {
            'none': '',
            'skip': '!skip',
            'invalid': 'siof 5',
            'valid': 'hello 4 f >'
        }
        self.assertEqual([], handle_player_input(tests['none']))
        self.assertEqual('!skip', handle_player_input(tests['skip']))
        self.assertEqual([], handle_player_input(tests['invalid']))
        self.assertEqual(('hello', 3, 14, 'left'), handle_player_input(tests['valid']))
            



if __name__ == '__main__':
    unittest.main()


