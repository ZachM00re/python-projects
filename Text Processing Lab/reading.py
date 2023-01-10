# reading.py
# Zachary Moore
# CSCI 111, Fall 2022
# Calculates text data and reading level of text files using various methods

import string

moby = open('moby_dick.txt',encoding = 'utf8')
green_eggs = open('green_eggs_and_ham.txt',encoding = 'utf8')
war = open('war_and_peace.txt',encoding = 'utf8')

in_word = False
in_sentence = False
in_syllable = False

letter_count = 0
word_count = 0
sentence_count = 0
syllable_count = 0


def initialize(): # resets all global booleans and counting variables
    global in_word,in_sentence,in_syllable,word_count,sentence_count,syllable_count,letter_count
    
    in_word = False
    in_sentence = False
    in_syllable = False
    letter_count = 0
    word_count = 0
    sentence_count = 0
    syllable_count = 0

def begin_word(character): # signifies the beginning of a word by detecting letters
    global in_word
    return not in_word and (character in string.ascii_letters)

def end_word(character): # signifies the end of a word by detecting non-letters
    global in_word
    return in_word and (character not in string.ascii_letters)

def begin_sentence(character): # signifies the beginning of a sentence by detecting capital letters
    global in_sentence
    return not in_sentence and (character in string.ascii_uppercase)

def end_sentence(character): # signifies the end of a sentence by detecting ending punctuation
    global in_sentence
    return in_sentence and (character in '.!?')

def begin_syllable(character): # signifies the beginning of a syllable by detecting vowels
    global in_syllable
    return not in_syllable and (character in 'aeiou')

def end_syllable(character): # signifies the end of a syllable by detecting non-vowels
    global in_syllable
    return in_syllable and (character not in 'aeiou')


def flesch_kincaid_grade_level(words,sentences,syllables):
    return 11.8 * (syllables/words) + 0.39 * (words/sentences) - 15.59

def flesch_reading_ease(words,sentences,syllables):
    return 206.835 - 84.6 * (syllables/words) - 1.015 * (words/sentences)

def automated_readability_index(letters,words,sentences):
    return 4.71 * (letters/words) + 0.5 * (words/sentences) - 21.43

def coleman_liau_index(letters,words,sentences):
    return 5.88 * (letters/words) - 29.6 * (sentences/words) - 15.8


def process_file(file_name):
    global in_word,word_count,in_sentence,sentence_count,in_syllable,syllable_count,letter_count

    initialize()
    
    begin = 0 # binary variable signifying when actual text begins

    for line in file_name:
        
        if '*** START' not in line and begin == 0: # skips unneccessary characters with file before text
            a = 'dummy'

        elif '*** START' in line and begin == 0:
            begin = 1

        elif '*** START' not in line and begin == 1: # true when within actual text and after START line
            
            for character in line:
                if '*** END' in line: # outputs data prior to iterating through END line
                    print('Letters:',letter_count,
                          '\nWords:',word_count,
                          '\nSentences:',sentence_count,
                          '\nSyllables:',syllable_count,
                          '\nFKG:',flesch_kincaid_grade_level(word_count,sentence_count,syllable_count),
                          '\nFRE:',flesch_reading_ease(word_count,sentence_count,syllable_count),
                          '\nARI:',automated_readability_index(letter_count,word_count,sentence_count),
                          '\nCLI:',coleman_liau_index(letter_count,word_count,sentence_count))
                    break
                
                if begin_word(character):
                    in_word = True

                    if begin_sentence(character): # a sentence can ONLY begin at beginning of word
                        in_sentence = True

                    if begin_syllable(character): # a syllable can begin at beginning of word
                        in_syllable = True
                    
                if end_word(character):
                    in_word = False
                    word_count += 1

                    if end_sentence(character): # a sentence can ONLY end at end of word
                        in_sentence = False
                        sentence_count += 1

                    if end_syllable(character): # a syllable can end at end of word
                        in_syllable = False
                        syllable_count += 1

                if character in string.ascii_letters: # counts all letters
                    letter_count += 1

                if begin_syllable(character): # some syllables begin in the middle of words
                    in_syllable = True
                    
                if end_syllable(character): # some syllables end in the middle of words
                    in_syllable = False
                    syllable_count += 1
         

print('Moby Dick')
process_file(moby)
print('\n')

print('Green Eggs and Ham')
process_file(green_eggs)
print('\n')

print('War and Peace')
process_file(war)
print('\n')

    

