import numpy as np



class Crossword(object):
    """docstring for Crossword"""
    def __init__(self, crossword_width,filepath):
        super(Crossword, self).__init__()
        self.crossword_width = crossword_width
        self.crossword_array = self.CreateCrosswordArray(crossword_width)

        self.crossword_clue_dict_list = self.CrosswordFileToClueDictList(filepath)
        self.clues = self.MakeClueList(self.crossword_clue_dict_list)
        self.crossword_array = self.PopulateCrosswordArray(self.crossword_array,self.clues)
        
    def CrosswordFileToClueDictList(self,filepath):
        clues_dict_list=[]
        file_text=""
        with open(filepath,"r") as f:
            file_text = f.read()

        split_text = file_text.split("\n")
        for line in split_text:
            if line == "":
                continue

            comma_split_text = line.split(",")
            clues_dict_list.append({"x_coord":comma_split_text[0],
                "y_coord":comma_split_text[1],
                "word_length":comma_split_text[2],
                "direction":comma_split_text[3],
                "clue_text":comma_split_text[4]})

        return clues_dict_list   


    def CreateCrosswordArray(self,crossword_width):       
        crossword_array = [[None]*crossword_width for value in range(crossword_width)]
        
        return np.array(crossword_array, dtype=object)    


    def CrosswordPrettyPrint(self):
        for row in self.crossword_array:
            row_string=""
            for value in row:
                if value == None:
                    row_string+="N"
                elif value == "":
                    row_string += "_"
                else:
                    row_string+=str(value)
            print(row_string)


    def MakeClueList(self,crossword_clue_dict_list):
        clues = []
        for clue_dict in crossword_clue_dict_list:
            clues.append(Clue(int(clue_dict["word_length"]),[int(clue_dict["x_coord"]),int(clue_dict["y_coord"])],clue_dict["direction"],clue_dict["clue_text"]))

        return clues


    def PopulateCrosswordArray(self,crossword_array,clues):
        for new in clues:
            crossword_array[new.word_row[0]:new.word_row[1],new.word_column[0]:new.word_column[1]] = ""

        return crossword_array


    def InsertWordIntoCrossword(self,clue,word):
        for letter_i in range(len(word)):
            clue_word_letter_row, clue_word_letter_column = clue.ClueLetterIndexToCrosswordIndex(letter_i)
            self.crossword_array[clue_word_letter_row,clue_word_letter_column] = word[letter_i]



class Clue(object):
    """docstring for Clue"""
    def __init__(self,word_length,word_starting_square,word_direction,clue_text, clue_type = "normal"):
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

    def ClueLetterIndexToCrosswordIndex(self,letter_index):
        row_i = self.word_row[0]
        column_i = self.word_column[0]

        if self.word_direction.lower() == "across":
            column_i += letter_index
        else:
            row_i += letter_index

        return (row_i,column_i)







        

if __name__ == '__main__':
    
    filepath = "crossword_clues_test.txt"
    

    crossword=Crossword(7,filepath)
    crossword.CrosswordPrettyPrint()
