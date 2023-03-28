"""
Author: Zachary Moore
Partner: John Schleider
File: evaluatorapp.py

View for the infix expression interpreter.
"""

from scanner import Scanner
from translator import Translator
from evaluator import Evaluator

def main():
    """Requests infix expressions, translates them to postfix,
    and evaluates them, until the user enters nothing."""
    while True:
        sourceStr = input("Enter an infix expression, or enter to quit: ")
        if sourceStr == "": break
        try:
            scanner = Scanner(sourceStr)
            translator = Translator(scanner)
            postfix = translator.translate()
            evaluator = Evaluator(postfix)
            print("Value:", evaluator.evaluate())
        except Exception as e:
            print("Error:", e, translator.translationStatus())

if __name__ == '__main__': 
    main()


