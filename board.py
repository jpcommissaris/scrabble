class Board:    

    def __init__(self, board):
        self.board = board
    
    def to_array(self):
        return self.board
    
    def add_inputs(self, inputs):
        word, row, col, direction = inputs
        for i, char in enumerate(word):
            if(direction=='left'):
                self.add(char, row, col+i)
            else:
                self.add(char, row+i, col)

    def add(self, letter, row, col):
        self.board[row][col] = letter
    
    def get(self, row, col):
        return self.board[row][col]

    def get_words(self):
        return self.__get_words_row() + self.__get_words_col()
    
    def __get_words_row(self):
        words = []
        for row in self.board:
            words_seperated = "".join(row).split('_')
            words += [word for word in words_seperated if len(word) > 1]
        return words
    
    def __get_words_col(self,):
        words = []
        columns = list(zip(*self.board))
        for col in columns:
            words_seperated = "".join(col).split('_')
            words += [word for word in words_seperated if len(word) > 1]
        return words
