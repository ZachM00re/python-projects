"""
vector.py
Zachary Moore
CSCI 111, Fall 2022
Module for 3D vector data structure
"""

import math

class V:
    """Represents 3D vector"""

    def __init__(self, x=0, y=0, z=0):
        self.x, self.y, self.z = x, y, z

    def __str__(self): # overrides print
        return ('V(%s, %s, %s)' % (round(self.x, 6),round(self.y, 6),round(self.z, 6))) # rounds to 6 decimal places if necessary

    def __add__(self, other):
        newVector = V()
        
        newVector.x, newVector.y, newVector.z = (self.x + other.x), (self.y + other.y), (self.z + other.z)
        
        return newVector

    def __sub__(self, other):
        newVector = V()
        
        newVector.x, newVector.y, newVector.z = (self.x - other.x), (self.y - other.y), (self.z - other.z)
        
        return newVector

    def __rmul__(self, other):  # right multiply - if vector class on the right of * operator
        newVector = V()

        newVector.x, newVector.y, newVector.z = (other * self.x), (other * self.y), (other * self.z)

        return newVector
        

    def __mul__(self, other):  # normal multiply - if vector class on the left of * operator
        newVector = V()
              
        if not isinstance(other, V) and isinstance(self, V):  # for multiplication of vector by a number
            
            newVector.x, newVector.y, newVector.z = (other * self.x), (other * self.y), (other * self.z)
            
            return newVector

        elif isinstance(self,V) and isinstance(other,V):  # for dot product of two vectors
            
            dotProd = (self.x * other.x) + (self.y * other.y) + (self.z * other.z)

            return dotProd
            

    def __truediv__(self, other):  # scalar division
        newVector = V()
        
        newVector.x, newVector.y, newVector.z = (self.x / other), (self.y / other), (self.z / other)

        return newVector
    

    def __eq__(self, other):
        
        if isinstance(self, V) and isinstance(other, V):  # modifies function of == for use with two vectors
            
            if math.isclose(self.x, other.x) and math.isclose(self.y, other.y) and math.isclose(self.z, other.z):  # checks equivalence of all vector components
                return True
            
            else:
                return False
        

    def __ne__(self, other):
        
        if math.isclose(self.x, other.x) and math.isclose(self.y, other.y) and math.isclose(self.z, other.z):  # modifies function of != for use with two vectors
            return False
        
        else:
            return True
        

    def __isub__(self, other):  # destructive subtraction
        
        self.x, self.y, self.z = (self.x - other.x), (self.y - other.y), (self.z - other.z)

        return self
    

    def __iadd__(self, other):  # destructive addition
        
        self.x, self.y, self.z = (self.x + other.x), (self.y + other.y), (self.z + other.z)
        
        return self
    

    def __imul__(self, other):  # destructive multiplication

        self.x, self.y, self.z = (other * self.x), (other * self.y), (other * self.z)
        
        return self
    

    def __itruediv__(self, other):  # destructive division
        
        self.x, self.y, self.z = (self.x / other), (self.y / other), (self.z / other)

        return self
    

    def __neg__(self):
        newVector = V()
        
        newVector.x, newVector.y, newVector.z = (-self.x), (-self.y), (-self.z)

        return newVector
    

    def __pos__(self):
        newVector = V()

        newVector.x, newVector.y, newVector.z  = (+self.x), (+self.y), (+self.z)
        
        return newVector
    

    def normalize(self):  # destructively returns unit vector of single input vector
        length = math.sqrt(self * self)

        if length == 0:
            raise RuntimeError('cannot normalize zero vector')
        
        else:
            self.x, self.y, self.z = (self.x / length), (self.y / length), (self.z / length)
            

    def project(self, other):  # nondestructively returns projection of self vector onto other vector

        if other == V(0, 0, 0):
            raise RuntimeError('cannot project onto zero vector')
        
        else:
            return (self * other) / (other * other) * other
        

    def gram_schmidt(self, v2, v3):

        # Testing for linear independence of new gram-schmidt vectors u1, u2, u3

        u1 = self
        length1 = math.sqrt(u1 * u1)
        
        u2 = v2 - v2.project(u1)
        length2 = math.sqrt(u2 * u2)
        
        u3 = v3 - v3.project(u1) - v3.project(u2)
        length3 = math.sqrt(u3 * u3)

        if math.isclose(length1,0) or math.isclose(length2,0) or math.isclose(length3,0):
            raise RuntimeError('cannot orthonormalize linearly dependent vectors')
        
        else:  # destructively returns normalized gram-schmidt vectors
            u1.normalize()
            u2.normalize()
            u3.normalize()

            self.x, self.y, self.z = u1.x, u1.y, u1.z
            v2.x, v2.y, v2.z = u2.x, u2.y, u2.z
            v3.x, v3.y, v3.z = u3.x, u3.y, u3.z
 

