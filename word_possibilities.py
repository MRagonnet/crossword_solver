from nltk.corpus import words as nltk_words
import re
import os

def GetWordList():
    dic_path = "google_dict.txt"

    dic_text = ""
    with open(dic_path,"r") as f:
        dic_text = f.read()

    word_list = dic_text.split(",")

    return word_list


def GetHunspellWordList():
    dic_path = os.path.join("hunspell-en_US","en_US.dic")

    dic_text = ""
    with open(dic_path,"r") as f:
        dic_text = f.read()

    word_list = dic_text.split("\n")

    
    word_list = [word.split("/")[0] for word in word_list[1:-1]]

    return word_list


def WordPossibilities(word_array, letter_possibilities=[]):
    # words_list = nltk_words.words()
    words_list = GetWordList()      

    regex_word = ""

    for char in word_array:
        if(char == ""):
            regex_word += "[a-z]"
        else:
            regex_word += char

    regex_template = re.compile("^"+regex_word+"$")

    words_of_correct_structure = [word for word in words_list if regex_template.match(word) != None]

    if(letter_possibilities == []):
        word_suggestions = words_of_correct_structure
    else:
        print(letter_possibilities)
        letter_possibilities = sorted(letter_possibilities)
        ordered_letters = "".join(letter_possibilities)
        print(ordered_letters)

        test_word = words_of_correct_structure[0]
        test_word = sorted(list(test_word))

        print("".join(test_word))

        word_suggestions = [word for word in words_of_correct_structure if "".join(sorted(list(word))) == ordered_letters]

    return word_suggestions



if __name__ == '__main__':
    #word = laptop
    word_list = GetWordList()
    print(word_list[0])
    correct_word = "eat"
    
    current_word = [""] * len(correct_word)
    current_word[2] = correct_word[2]

    print(current_word)

    current_word = [""] * 4
    current_word[0] = "b"
    current_word[1] = "a"
    # current_word[2] = "g"


    word_suggestions = WordPossibilities(current_word)#,list(correct_word))
    print(len(word_suggestions))
    print(word_suggestions)

