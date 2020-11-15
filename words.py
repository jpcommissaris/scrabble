import json

class Words:
    def __init__(self, filename):
        self.words = self.__generate(filename)
    
    def __generate(self, filename):
        with open(filename) as f: 
            return json.load(f)  
    
    def contains(self, word):
        return self.words.get(word, False)


