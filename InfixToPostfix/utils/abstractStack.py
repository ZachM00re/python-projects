"""
File: abstractStack.py
Author: Ken Lambert
"""

from .abstractCollection import AbstractCollection

class AbstractStack(AbstractCollection):
    """Represents an abstract stack."""

    def __init__(self, sourceCollection=None):
        """Initializes the stack at this level."""
        super().__init__(sourceCollection)

    def add(self, item):
        """For compatibility with other collections."""
        self.push(item)
