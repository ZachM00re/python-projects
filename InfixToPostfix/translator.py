"""
Author: Zachary Moore
File: translator.py
"""

from tokens import Token
from scanner import Scanner
from utils.linkedStack import LinkedStack

class Translator(object):
    """Translates infix expressions to postfix expressions."""

    def __init__(self, scanner):
        """Sets the initial state of the translator."""
        # Keeps track of the infix expression we've seen so far
        self._expressionSoFar = ""
        
        # Stack for operators
        self._operatorStack = LinkedStack()
        
        # Scanner to tokenize a string
        self._scanner = scanner


    def translate(self):
        """Returns a list of tokens that represent the postfix
        form of sourceStr.  Assumes that the infix expression
        in sourceStr is syntactically correct"""
        
        postfix = list()

        for currentToken in self._scanner:

            self._expressionSoFar += str(currentToken) + " "

            # Append operands to postfix
            
            if currentToken.getType() == Token.INT:
                postfix.append(currentToken)

            # Push left parentheses onto stack

            elif currentToken.getType() == Token.LPAR:
                self._operatorStack.push(currentToken)
                
            # If ), pop from the stack until we see a (

            elif currentToken.getType() == Token.RPAR:
                while self._operatorStack.peek().getType() != Token.LPAR:
                    postfix.append(self._operatorStack.pop())
                self._operatorStack.pop()   # Throw away left parenthesis

            # Handling operators
            
            else:
            
                if len(self._operatorStack) == 0:
                    self._operatorStack.push(currentToken)
                   
                else:     

                    while self._operatorStack.peek().getPrecedence() >= currentToken.getPrecedence():

                        # Handles right-associativity of EXP operator
                        
                        if self._operatorStack.peek().getType() == Token.EXP:
                            
                            if self._operatorStack.peek().getPrecedence() > currentToken.getPrecedence():
                                postfix.append(self._operatorStack.pop())

                                if len(self._operatorStack) == 0:
                                    break
                            else:
                                break
                            
                        # Handles precedence of all other operators
                        
                        else:              
                            postfix.append(self._operatorStack.pop())

                            if len(self._operatorStack) == 0:
                                break
                
                    # Finally, push the current token onto the stack
            
                    self._operatorStack.push(currentToken)
            
                
        # At the end, pop the remaining tokens from the stack and add to the end of postfix
        
        while len(self._operatorStack) != 0:
            postfix.append(self._operatorStack.pop())
        
        return postfix
   
    def __str__(self):
        """Returns a string containing the contents of the expression
        processed and the stack to this point."""
        result = "\n"
        
        if self._expressionSoFar == "":
            result += "Portion of expression processed: none\n"
        
        else: 
            result += "Portion of expression processed: " + \
                   self._expressionSoFar + "\n"
        
        if self._operatorStack.isEmpty():
            result += "The stack is empty"
        
        else:
            result += "Operators on the stack          : " + \
                      str(self._operatorStack)
        
        return result

    def translationStatus(self):
        return str(self)

    
def main():
    """Tester function for translators."""
    while True:
        sourceStr = input("Enter an infix expression, or enter to quit: ")
        if sourceStr == "":
            break
        else:
            try:
                translator = Translator(Scanner(sourceStr))
                postfix = translator.translate()
                print("Postfix:", end =" ")
                for token in postfix: print(token, end=" ")
                print()
            except Exception as e:
                print("Error: ", e, translator.translationStatus())

if __name__ == '__main__': 
    main()

