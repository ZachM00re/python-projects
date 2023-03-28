"""
File: scanner.py
A scanner for processing languages.
"""

from tokens import Token

class Scanner(object):
    """A scanner for simple languages."""

    EOE = ';'        # end-of-expression
    TAB = '\t'       # tab

    def __init__(self, sourceStr):
        self._sourceStr = sourceStr
        self._getFirstToken()

    def hasNextToken(self):
        """Returns True if there is a next token,
        or False otherwise."""
        return self._currentToken != None

    def nextToken(self):
        """Returns the next token.
        Precondition: hashNext returns True.
        Raises: Exception if hasNext returns False."""
        if not self.hasNextToken():
            raise Exception("There are no more tokens")            
        temp = self._currentToken
        self._getNextToken()
        return temp

    def __iter__(self):
        """Returns an iterator on self."""
        while self.hasNextToken():
            yield self.nextToken()

    def _getFirstToken(self):
        self._index = 0
        self._currentChar = self._sourceStr[0]
        self._getNextToken()
    
    def _getNextToken(self):
        self._skipWhiteSpace()
        if self._currentChar.isdigit():
            self._currentToken = Token(self._getInteger())
        elif self._currentChar == Scanner.EOE:
            self._currentToken = None
        else:
            self._currentToken = Token(self._currentChar)
            self._nextChar()
    
    def _nextChar(self):
        if self._index >= len(self._sourceStr) - 1:
            self._currentChar = Scanner.EOE
        else:
            self._index += 1
            self._currentChar = self._sourceStr[self._index]
    
    def _skipWhiteSpace(self):
        while self._currentChar in (' ', Scanner.TAB):
            self._nextChar()
    
    def _getInteger(self):
        num = 0
        while True:
            num = num * 10 + int(self._currentChar)
            self._nextChar()
            if not self._currentChar.isdigit():
                break
        return num


def test():
    """A simple tester program."""
    while True:
        sourceStr = input("Enter an expression: ")
        if sourceStr == "": break
        print("Token strings:")
        scanner = Scanner(sourceStr)
        for token in scanner:
            print(token)

if __name__ == '__main__': 
    test()

