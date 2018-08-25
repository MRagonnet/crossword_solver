import numpy as np

class Crossword(object):
    """docstring for Crossword"""
    def __init__(self, crossword_width):
        super(Crossword, self).__init__()
        self.crossword_width = crossword_width
        self.crossword_array = self.CreateCrosswordArray(crossword_width)
        self.crossword_array = self.PopulateCrosswordArray(self.crossword_array)

    def CreateCrosswordArray(self,crossword_width):       
        crossword_array = [[None]*crossword_width for value in range(crossword_width)]
        
        return np.array(crossword_array)    

    def CrosswordPrettyPrint(self):
        for row in self.crossword_array:
            print(row)

    #def MakeClueList:

    def PopulateCrosswordArray(self,crossword_array):
        new = Clue("normal",6,[2,2],"down","an eminently fuckable boy")
        
        print(crossword_array[new.word_row[0]:new.word_row[1]][new.word_column[0]:new.word_column[1]])
        print("")
        print(crossword_array[2:8,2])
        print("")
        
        crossword_array[new.word_row[0]:new.word_row[1],new.word_column[0]:new.word_column[1]] = 0

        return crossword_array


class Clue(object):
    """docstring for Clue"""
    def __init__(self, clue_type,word_length,word_starting_square,word_direction,clue_text):
        super (Clue, self).__init__()
        self.clue_type = clue_type
        self.word_length = word_length
        self.word_starting_square = word_starting_square
        self.word_direction = word_direction
        self.clue_text = clue_text

        self.word_row,self.word_column = self.CalculateWordLocation(word_starting_square,word_direction,word_length)

    def CalculateWordLocation(self, word_starting_square,word_direction,word_length):
        row,column = word_starting_square
        if word_direction.lower() == "across":
            word_row = (row, row+1)
            word_column = (column,column+word_length)
        else:
            word_row = (row,row+word_length)
            word_column = (column,column+1)


        return word_row,word_column






        

if __name__ == '__main__':
    crossword=Crossword(10)
    crossword.CrosswordPrettyPrint()
