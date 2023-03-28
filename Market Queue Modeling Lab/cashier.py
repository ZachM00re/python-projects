"""
File: cashier.py
Author: Ken Lambert

Edits by Zachary Moore

Models multiple cashiers.
"""

from utils.linkedQueue import LinkedQueue

class Cashier(object):
    """Represents a cashier."""

    def __init__(self, number):
        """Maintains a cashier number, a queue of customers,
        number of customers served, total customer wait time,
        and a current customer being processed."""
        self._number = number
        self._totalCustomerWaitTime = 0
        self._customersServed = 0
        self._currentCustomer = None
        self._queue = LinkedQueue()

    def addCustomer(self, c):
        """Adds an arriving customer to my line."""
        self._queue.add(c)
    
    def customersInLine(self):
        return len(self._queue)
   
    def serveCustomers(self, currentTime):
        """Serves my customers during a given unit of time."""
        if self._currentCustomer is None:
            # No customers yet
            if self._queue.isEmpty():
                return
            else:
                # Select first waiting customer and tally results
                self._currentCustomer = self._queue._front.data  # Changed to NOT pop customer before starting service
                self._totalCustomerWaitTime += \
                                            currentTime - \
                                            self._currentCustomer.arrivalTime()

        # Give a unit of service
        self._currentCustomer.serve()

        # If current customer is finished, send it away   
        if self._currentCustomer.amountOfServiceNeeded() == 0:
            self._currentCustomer = self._queue.pop()  # Pops customer only after receiving FULL service
            self._customersServed += 1
            self._currentCustomer = None
   
    def __str__(self):
        """Returns my results: my number, my total customers served,
        my average wait time per customer, and customers left on my queue."""
        if self._customersServed != 0:
            aveWaitTime = float(self._totalCustomerWaitTime) /\
                          self._customersServed
        else:
            aveWaitTime = 0.0
        result = "%4d %8d %13.2f %8d" % (self._number,
                                         self._customersServed,
                                         aveWaitTime,
                                         len(self._queue))
        return result
