"""
File: arrayStack.py
Author: Zachary Moore
Partner: John Schleider
"""

from .abstractStack import AbstractStack
from .arrays import Array

class ArrayStack(AbstractStack):
    """Represents a link-based stack."""
    
    DEFAULT_CAPACITY = 10

    def __init__(self, sourceCollection = None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._items = Array(ArrayStack.DEFAULT_CAPACITY)
        super().__init__(sourceCollection)

    def peek(self):
        """Returns the item at the top of the stack.
        Precondition: the stack is not empty.
        Raises: KeyError if stack is empty."""
        if self.isEmpty():
            raise ValueError("Attempt to peek at empty stack")
        return self._items[len(self) - 1]

    def __iter__(self):
        """Supports iteration over a view of self, from bottom to top."""
        index = 0 
        modCount = self.getModCount()
        while index < len(self):
            yield self._items[index]
            if modCount != self.getModCount():
                raise AttributeError("Mutations not allowed in a for loop")
            index += 1

    # Mutator methods
    
    def grow(self):
        newItems = Array(len(self._items) * 2)
        index = 0
        for item in self:
            newItems[index] = item
            index += 1
        
        self._items = newItems
    
    def shrink(self):
        if len(self._items) // 2 >= ArrayStack.DEFAULT_CAPACITY:
            newItems = Array(len(self._items) // 2)
            index = 0
            for item in self:
                newItems[index] = item
                index += 1
            
            self._items = newItems
            
    def clear(self):
        """Makes self become empty."""
        self.resetSizeAndModCount()
        self._items = Array(ArrayStack.DEFAULT_CAPACITY)        

    def push(self, item):
        """Inserts item at top of the stack."""
        if len(self) == len(self._items):
            self.grow()
        self._items[len(self)] =  item
        self._size += 1
        self.incModCount()

    def pop(self):
        """Removes and returns the item at the top of the stack.
        Precondition: the stack is not empty.
        Raises: KeyError if stack is empty.
        Postcondition: the top item is removed from the stack."""
        if self.isEmpty():
            raise ValueError("Attempt to pop from empty stack")
        if len(self) <= len(self._items) // 4:
            self.shrink()
        data = self._items[len(self) - 1]
        self._size -= 1
        self.incModCount()
        return data


def test():
    """Tests a linked stack."""
    stack = ArrayStack(range(5))
    print("Expect [0, 1, 2, 3, 4]: ", stack)
    clone = ArrayStack(stack)
    print("Expect True:", stack == clone)

if __name__ == '__main__': 
    test()
