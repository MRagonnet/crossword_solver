from crossword_representation import Crossword

from word_possibilities import WordPossibilities

import numpy as np

class ExhaustiveCrosswordSolver(object):
    """docstring for ExhaustiveCrosswordSolver"""
    def __init__(self, crossword_width,clues_file_path):
        super(ExhaustiveCrosswordSolver, self).__init__()
        self.crossword = Crossword(crossword_width,clues_file_path)

        self.possible_words_lists = []
        self.UpdatePossibleWords()

        self.clue_letter_track_arrays = []
        for clue_i in range(len(self.crossword.clues)):
            self.clue_letter_track_arrays.append(self.CreateLetterTrackArray())

        self.aggregated_letter_track_array = self.CreateLetterTrackArray()
        
        self.UpdateLetterTrackArray()

        print(self.aggregated_letter_track_array)

        

    def UpdatePossibleWords(self):
        self.possible_words_lists = []

        for clue_i in range(len(self.crossword.clues)):
            clue = self.crossword.clues[clue_i]

            #TODO replace with class based function call
            clue_word = self.crossword.crossword_array[clue.word_row[0]:clue.word_row[1],clue.word_column[0]:clue.word_column[1]].reshape(-1)
            clue_word = list(clue_word)
            
            self.possible_words_lists.append(WordPossibilities(clue_word))

    def CreateLetterTrackArray(self):
        crossword_width = self.crossword.crossword_width
        return np.array([[set([]) for value in range(crossword_width)] for value in range(crossword_width)], dtype=object)

    def UpdateLetterTrackArray(self):
        for clue_i in range(len(self.crossword.clues)):
            clue = self.crossword.clues[clue_i]
            possible_words = self.possible_words_lists[clue_i]

            for possible_word in possible_words:
                for letter_i in range(len(possible_word)):
                    clue_word_letter_row, clue_word_letter_column = self.ClueLetterIndexToCrosswordIndex(clue, letter_i)
                    self.clue_letter_track_arrays[clue_i][clue_word_letter_row,clue_word_letter_column].add(possible_word[letter_i])
        
        self.AggregateLetterTracking()

    def AggregateLetterTracking(self):
        for row_i in range(self.crossword.crossword_width):
            for column_i in range(self.crossword.crossword_width):
                for clue_track_i in range(len(self.clue_letter_track_arrays)):
                    if(len(self.clue_letter_track_arrays[clue_track_i][row_i,column_i]) > 0):
                            
                        if(len(self.aggregated_letter_track_array[row_i,column_i]) == 0):
                            self.aggregated_letter_track_array[row_i,column_i] = self.clue_letter_track_arrays[clue_track_i][row_i,column_i]
                        else:
                            # print("aggregate")
                            # print(self.aggregated_letter_track_array[row_i,column_i])
                            # print(self.clue_letter_track_arrays[clue_track_i][row_i,column_i])
                            # print("")
                            self.aggregated_letter_track_array[row_i,column_i] = self.aggregated_letter_track_array[row_i,column_i].intersection(self.clue_letter_track_arrays[clue_track_i][row_i,column_i])


    def ClueLetterIndexToCrosswordIndex(self,clue,letter_index):
        row_i = clue.word_row[0]
        column_i = clue.word_column[0]

        if clue.word_direction.lower() == "across":
            column_i += letter_index
        else:
            row_i += letter_index

        return (row_i,column_i)

        # for each clue, generate the list of possible words
        # for each tile, track the possible letters. 
        # use the limitations of the letters to eliminate some words
        # when searching, choose a word to place and update possible words for each clue

        #loop until complete:
            #loop until stable:
                # update possible words
                # update possible letters
            #choose a word, if no words left, back up

if __name__ == '__main__':
    crossword_width = 7
    file_path = "crossword_clues_test.txt"

    solver = ExhaustiveCrosswordSolver(crossword_width,file_path)
