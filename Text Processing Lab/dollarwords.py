# dollarwords.py
# Zachary Moore
# CSCI 111, Fall 2022
# Assigns cent value to ASCII letters and determines how many words contain characters worth 1 dollar

words = open('words.txt')

import string

def letter_value(c): # converts upper and lowercase versions of letters to same cent "value" 

    value = 0
    
    if c in string.ascii_letters:
        if ord(c) < 91:
            value = ord(c) - 64 # converts capital letters
        else:
            value = ord(c) - 96 # converts lowercase letters
            
    return value

def word_value(w): # calculates cent value of entire word

    word_total = 0
    
    for letter in w:
        word_total = word_total + letter_value(letter)
    return word_total

def is_dollar_word(w): # determines whether a word is a "dollar word"
    
    if word_value(w) == 100:
        return True
    else:
        return False

def total_count():
    
    dollar_count = 0
    total_count = 0
    
    for word in words:

        total_count += 1 # determines length of txt file
        
        if is_dollar_word(word) == True: # counts number of words worth $1
            dollar_count += 1

    print('Total number of words:',total_count,
          '\nTotal number worth $1:',dollar_count,
          '\nPercentage of total  :',(dollar_count / total_count) * 100)

total_count()

        
                                                    














    
