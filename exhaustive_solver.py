from crossword_representation import Crossword

from word_possibilities import WordPossibilities

import numpy as np

class ExhaustiveCrosswordSolver(object):
    """docstring for ExhaustiveCrosswordSolver"""
    def __init__(self, crossword_width,clues_file_path):
        super(ExhaustiveCrosswordSolver, self).__init__()
        self.crossword = Crossword(crossword_width,clues_file_path)

        self.unsolved_clues = list(range(len(self.crossword.clues)))

        self.possible_words_lists = []
        self.tried_words_lists = [[] for i in range(len(self.unsolved_clues))]
        self.UpdatePossibleWords()

        self.clue_letter_track_arrays = []
        for clue_i in range(len(self.crossword.clues)):
            self.clue_letter_track_arrays.append(self.CreateLetterTrackArray())

        self.aggregated_letter_track_array = self.CreateLetterTrackArray()
        
        self.UpdateLetterTrackArray()

        self.Solve()
        

    def UpdatePossibleWords(self):
        self.possible_words_lists = []

        for clue_i in range(len(self.crossword.clues)):
            clue = self.crossword.clues[clue_i]

            #TODO replace with class based function call
            clue_word = self.crossword.crossword_array[clue.word_row[0]:clue.word_row[1],clue.word_column[0]:clue.word_column[1]].reshape(-1)
            clue_word = list(clue_word)
            
            all_words = WordPossibilities(clue_word)
            filtered_words = [word for word in all_words if word not in self.tried_words_lists[clue_i]]

            self.possible_words_lists.append(filtered_words)

    def CreateLetterTrackArray(self):
        crossword_width = self.crossword.crossword_width
        return np.array([[set([]) for value in range(crossword_width)] for value in range(crossword_width)], dtype=object)

    def UpdateLetterTrackArray(self):
        print("update letter track")
        for clue_i in range(len(self.crossword.clues)):
            clue = self.crossword.clues[clue_i]
            possible_words = self.possible_words_lists[clue_i]
            print("possible words for clue:"+str(clue_i),len(possible_words))
            for possible_word in possible_words:
                for letter_i in range(len(possible_word)):
                    clue_word_letter_row, clue_word_letter_column = self.ClueLetterIndexToCrosswordIndex(clue, letter_i)
                    self.clue_letter_track_arrays[clue_i][clue_word_letter_row,clue_word_letter_column].add(possible_word[letter_i])
        
        self.AggregateLetterTracking()
        print("")


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

    def GetLetterTrackSetSizeArray(self):
        crossword_width = self.crossword.crossword_width
        size_track_array = np.array([[0 for value in range(crossword_width)] for value in range(crossword_width)], dtype=object)

        for row_i in range(self.crossword.crossword_width):
            for column_i in range(self.crossword.crossword_width):
                size_track_array[row_i,column_i] = len(self.aggregated_letter_track_array[row_i,column_i])

        return size_track_array        


    def Solve(self):

        steps_taken_list = []
        
        solve_break_count = 0
        solve_count_limit = 100

        back_up_count = 0

        while (len(self.unsolved_clues) > 0):
            solve_break_count += 1

            aggregates_updating = True

            previous_set_lengths = self.GetLetterTrackSetSizeArray()

            break_count = 0 
            count_limit = 100
            while(aggregates_updating):
                break_count += 1
                
                self.UpdateLetterTrackArray()

                self.UpdatePossibleWords()


                if(np.array_equal(previous_set_lengths, self.GetLetterTrackSetSizeArray())):
                    aggregates_updating = False

                if(break_count >= count_limit):
                    print("aggregation break count reached")
                    print("")
                    break

            if(len(self.possible_words_lists[self.unsolved_clues[0]]) == 0):
                back_up = True
            else:
                least_words_clue_index = self.unsolved_clues[0]
                current_least_words = len(self.possible_words_lists[least_words_clue_index])

                back_up = False

                for clue_check_i in range(1,len(self.unsolved_clues)):
                    clue_i = self.unsolved_clues[clue_check_i]
                    if(len(self.possible_words_lists[clue_i]) == 0):
                        back_up = True
                        break

                    if(len(self.possible_words_lists[clue_i]) < current_least_words):
                        current_least_words = len(self.possible_words_lists[clue_i])
                        least_words_clue_index = clue_i

            if(back_up):
                print("backing up")
                print("len(steps_taken_list)",len(steps_taken_list))
                back_up_count += 1
                back_up_step = steps_taken_list.pop(-1)
                self.unsolved_clues.append(back_up_step[0])
                self.clue_letter_track_arrays = back_up_step[2][:]
                self.tried_words_lists = back_up_step[3][:]
                self.crossword.crossword_array = back_up_step[4][:]

            else:
                print(least_words_clue_index)
                print(len(self.possible_words_lists[least_words_clue_index]))

                chosen_word = self.possible_words_lists[least_words_clue_index][0]
                print("chosen_word",chosen_word)
                
                self.tried_words_lists[least_words_clue_index].append(chosen_word)
                steps_taken_list.append( (least_words_clue_index,chosen_word,np.copy(self.clue_letter_track_arrays),np.copy(self.tried_words_lists),np.copy(self.crossword.crossword_array))  )

                print("least_words_clue_index",least_words_clue_index)
                self.possible_words_lists[least_words_clue_index] = [chosen_word]
                print(self.possible_words_lists[least_words_clue_index])
                self.unsolved_clues.remove(least_words_clue_index)

                self.crossword.InsertWordIntoCrossword( self.crossword.clues[least_words_clue_index], chosen_word)


            if(solve_break_count >= solve_count_limit):
                print("aggregation break count reached")
                print("")
                break
          

        print("crossword solved")
        print("")

        print("back_up_count",back_up_count)
        for clue_i in range(len(self.possible_words_lists)):
            clue = self.crossword.clues[clue_i]
            print(len(self.possible_words_lists[clue_i]))
            clue_word = self.crossword.crossword_array[clue.word_row[0]:clue.word_row[1],clue.word_column[0]:clue.word_column[1]].reshape(-1)
            print("".join(clue_word))
            # print(self.possible_words_lists[clue_i][0])
            # self.crossword.InsertWordIntoCrossword( self.crossword.clues[clue_i], self.possible_words_lists[clue_i][0] )

        self.crossword.CrosswordPrettyPrint()


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
