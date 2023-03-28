"""
File: marketModel.py
Author: Ken Lambert

Edits by Zachary Moore

Models multiple cashiers.
"""

from cashier import Cashier
from customer import Customer
import random

class MarketModel(object):

    def __init__(self, lengthOfSimulation, averageTimePerCus,
                 probabilityOfNewArrival, numCashiers):
        self._probabilityOfNewArrival = probabilityOfNewArrival
        self._lengthOfSimulation = lengthOfSimulation
        self._averageTimePerCus = averageTimePerCus
        self._cashiers = list() # Allows for multiple cashiers

        for i in range(numCashiers):
            self._cashiers.append(Cashier(i+1))
        
    def runSimulation(self):
        """Run the clock for n ticks."""
        
        for currentTime in range(self._lengthOfSimulation):
            
            # Attempts to generate a new customer
            
            customer = Customer.generateCustomer(
                self._probabilityOfNewArrival,
                currentTime,
                self._averageTimePerCus)
            
            # If successfully generated, sends a customer to a cashier
            
            if customer != None:

                # Customer first goes to random cashier
                
                randCashier = random.randint(0,len(self._cashiers)-1)
                shortestLine = randCashier
                length = self._cashiers[randCashier].customersInLine()

                # Customer moves to nearby line if shorter than random choice line

                for i in range(1,3):

                    left = randCashier - i
                    right = randCashier + i
                    
                    if left >= 0:
                            
                        if self._cashiers[left].customersInLine() < length:
            
                            shortestLine = left
                            length = self._cashiers[left].customersInLine()
                                
                    if right <= len(self._cashiers) - 1:
                            
                        if self._cashiers[right].customersInLine() < length:
                            shortestLine = right
                            length = self._cashiers[right].customersInLine()

                self._cashiers[shortestLine].addCustomer(customer)
 

                # Tells all cashiers to provide another unit of service, if able
            
                for c in self._cashiers:
                    if c.customersInLine() != 0:
                        c.serveCustomers(currentTime)
            
    def __str__(self):
        """Returns the string rep of the results of the simulation."""

        output = str()

        for c in self._cashiers:
            output = output + "\n " + str(c)

        return "CASHIER CUSTOMERS   AVERAGE     LEFT IN\n" + \
               "        PROCESSED   WAIT TIME   LINE\n" + \
               output
