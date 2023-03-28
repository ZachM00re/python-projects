"""
Author: Zachary Moore
Partner: John Schleider
File: evaluator.py
"""

from tokens import Token
from scanner import Scanner
from utils.linkedStack import LinkedStack
import math

class Evaluator(object):
    """Evaluator for postfix expressions.
    Assumes that the input is a syntactically correct
    sequence of tokens."""
   
    def __init__(self, scanner):
        """Sets the initial state of the evaluator."""
        # Stacks for operands
        self._operandStack = LinkedStack()
        
        # Scanner for scanning a string into tokens, OR a list of tokens
        self._scanner = scanner

    def evaluate(self):
        """Returns the value of the postfix expression."""
        # For each token in our scanner or list,
        # If it's an operand, push the token
        # If it's an operator pop off two tokens from the stack,
        #  compute the value, and then push the value back on the stack
        for currentToken in self._scanner:
            if currentToken.getType() == Token.INT:
                self._operandStack.push(currentToken)
                
            elif currentToken.isOperator(): 
                right = self._operandStack.pop()
                left = self._operandStack.pop()
                result = Token(self._computeValue(currentToken,
                                                  left.getValue(),
                                                  right.getValue()))
                self._operandStack.push(result)
        
        # The result is the last thing left in the stack
        result = self._operandStack.pop()
        return result.getValue()   

    def _computeValue(self, op, value1, value2):
        """Utility routine to compute a value."""
        
        result = 0
        theType = op.getType()
        # Use python's application of an operator depending on theType of the token
        if theType == Token.PLUS:
            result = value1 + value2
        elif theType == Token.MINUS:
            result = value1 - value2
        elif theType == Token.MUL:
            result = value1 * value2
        elif theType == Token.DIV:
            if value2 == 0:
                raise ZeroDivisionError("Attempt to divide by 0")
            else:
                result = value1 // value2
        elif theType == Token.MOD:
            result = value1 % value2
        elif theType == Token.EXP:
            result = value1 ** value2
                
        return result

def main():
    """Tester function for the evaluator."""
    while True:
        sourceStr = input("Enter a postfix expression, or enter to quit: ")
        if sourceStr == "": break
        try:
            evaluator = Evaluator(Scanner(sourceStr))
            print("The value is", evaluator.evaluate())
        except Exception as e:
            print("Exception:", str(e))

if __name__ == '__main__': 
    main()
            


