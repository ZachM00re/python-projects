"""
test_vector.py
Zachary Moore
CSCI 111, Fall 2022
Tests 3D vector operations from vector.py (if saved in same folder)
"""

import unittest, vector, math

class Test_Addition(unittest.TestCase):
    def test_addition(self):

        # Test 1

        v1 = vector.V(1,2,3)
        v2 = vector.V(10,20,30)
        self.assertEqual(v1 + v2,vector.V(11,22,33))

        # Test 2

        v3 = vector.V(-1,-2,-3)
        v4 = vector.V(-10,-20,-30)
        self.assertEqual(v3 + v4,vector.V(-11,-22,-33))

        
class Test_Subtraction(unittest.TestCase):
    def test_subtraction(self):

        # Test 1
        
        v1 = vector.V(1,2,3)
        v2 = vector.V(10,20,30)
        self.assertEqual(v1 - v2,vector.V(-9,-18,-27))

        # Test 2

        v3 = vector.V(-1,-2,-3)
        v4 = vector.V(-10,-20,-30)
        self.assertEqual(v3 - v4,vector.V(9,18,27))
        

class Test_RightMult(unittest.TestCase):
    def test_rightmult(self):

        # Test 1

        v1 = vector.V(1,2,3)
        self.assertEqual(5 * v1,vector.V(5,10,15))

        # Test 2

        v2 = vector.V(-1,-2,-3)
        self.assertEqual(5 * v2,vector.V(-5,-10,-15))
        

class Test_Mult(unittest.TestCase):
    def test_mult(self):

        # Test 1
        
        v1 = vector.V(1,2,3)
        self.assertEqual(v1 * 5,vector.V(5,10,15))

        # Test 2

        v2 = vector.V(-1,-2,-3)
        self.assertEqual(v2 * 5,vector.V(-5,-10,-15))
        

class Test_TrueDiv(unittest.TestCase):
    def test_truediv(self):

        # Test 1
        
        v1 = vector.V(1,2,3)
        self.assertEqual(v1 / 2,vector.V(0.5,1,1.5))

        # Test 2

        v2 = vector.V(-1,-2,-3)
        self.assertEqual(v2 / 2,vector.V(-0.5,-1,-1.5))
        

class Test_Equal(unittest.TestCase):
    def test_equal(self):

        # Test 1
    
        v1 = vector.V(1,2,3)
        v2 = vector.V(1,2,3)
        self.assertEqual(v1 == v2, True)

        # Test 2

        v3 = vector.V(-5,-4,3)
        v4 = vector.V(-5,-4,3)
        self.assertEqual(v3 == v4, True)

        # Test 3

        v5 = vector.V(-5,-4,3)
        v6 = vector.V(-5,4,-3)
        self.assertEqual(v5 == v6, False)
        

class Test_NotEqual(unittest.TestCase):
    def test_notequal(self):

        # Test 1
    
        v1 = vector.V(1,2,3)
        v2 = vector.V(1,2,4)
        self.assertEqual(v1 != v2, True)

        # Test 2

        v3 = vector.V(-5,4,3)
        v4 = vector.V(-5,4,-3)
        self.assertEqual(v3 != v4, True)

        # Test 3

        v5 = vector.V(-5,4,3)
        v6 = vector.V(-5,4,3)
        self.assertEqual(v5 != v6, False)
        

class Test_DestructSub(unittest.TestCase):
    def test_destructsub(self):

        # Test 1
        
        v1 = vector.V(1,2,3)
        v2 = vector.V(10,20,30)
        v1 -= v2
        self.assertEqual(v1, vector.V(-9,-18,-27))

        # Test 2

        v3 = vector.V(-1,-2,-3)
        v4 = vector.V(-10,-20,-30)
        v3 -= v4
        self.assertEqual(v3, vector.V(9,18,27))
        

class Test_DestructAdd(unittest.TestCase):
    def test_destructadd(self):

        # Test 1
        
        v1 = vector.V(1,2,3)
        v2 = vector.V(10,20,30)
        v1 += v2
        self.assertEqual(v1,vector.V(11,22,33))

        # Test 2

        v3 = vector.V(-1,-2,-3)
        v4 = vector.V(-10,-20,-30)
        v3 += v4
        self.assertEqual(v3,vector.V(-11,-22,-33))
        
        

class Test_DestructMult(unittest.TestCase):
    def test_destructmuklt(self):

        # Test 1
        
        v1 = vector.V(1,2,3)
        v1 *= 5
        self.assertEqual(v1,vector.V(5,10,15))

        # Test 2

        v2 = vector.V(-1,-2,-3)
        v2 *= 5
        self.assertEqual(v2,vector.V(-5,-10,-15))
        

class Test_DestructDiv(unittest.TestCase):
    def test_destructdiv(self):

        # Test 1
        
        v1 = vector.V(1,2,3)
        v1 /= 2
        self.assertEqual(v1,vector.V(0.5,1,1.5))

        # Test 2

        v2 = vector.V(-1,-2,-3)
        v2 /= 2
        self.assertEqual(v2,vector.V(-0.5,-1,-1.5))

        
class Test_Neg(unittest.TestCase):
    def test_neg(self):
        v1 = vector.V(1,2,3)

        self.assertEqual(-v1,vector.V(-1,-2,-3))
        

class Test_Pos(unittest.TestCase):
    def test_pos(self):

        # Test 1
        
        v1 = vector.V(1,2,3)
        self.assertEqual(+v1,vector.V(1,2,3))

        # Test 2

        v2 = vector.V(-1,-2,-3)
        self.assertEqual(+v2,vector.V(-1,-2,-3))
        

class Test_Normalize(unittest.TestCase):
    def test_normalize(self):

        # Test 1
    
        v1 = vector.V(1,2,2) # using pythagorean quadruples to avoid rounding errors
        v1.normalize()
        self.assertEqual(v1,vector.V(1/3,2/3,2/3))

        # Test 2

        v2 = vector.V(2,3,6)
        v2.normalize()
        self.assertEqual(v2,vector.V(2/7,3/7,6/7))

        # Test 3

        v3 = vector.V(12,16,21)
        v3.normalize()
        self.assertEqual(v3,vector.V(12/29,16/29,21/29))
        

class Test_Projection(unittest.TestCase):
    def test_projection(self):

        # Test 1
    
        v1 = vector.V(1,2,2)
        v2 = vector.V(2,3,6)
        self.assertEqual(v1.project(v2),vector.V(20/49*2, 20/49*3, 20/49*6)) # using pythagorean quadruples to avoid rounding errors

        # Test 2
    
        v3 = vector.V(1,4,8)
        v4 = vector.V(4,4,7)
        self.assertEqual(v3.project(v4),vector.V(76/81*4, 76/81*4, 76/81*7))

        # Test 3
                         
        v5 = vector.V(2,6,9)
        v6 = vector.V(6,6,7)
        self.assertEqual(v5.project(v6),vector.V(111/121*6, 111/121*6, 111/121*7))


        # Test 4

        v5 = vector.V(0,0,0)
        v6 = vector.V(6,6,7)
        self.assertEqual(v5.project(v6),vector.V(0, 0, 0))


class Test_GramSchmidt(unittest.TestCase):
    def test_gramschmidt(self):

        # Test 1 (from lab instructions)
    
        v1 = vector.V(1,1,1)*3
        v2 = vector.V(1,-2,3)*4
        v3 = vector.V(1,3,-2)*5

        v1.gram_schmidt(v2,v3)

        for v in (v1,v2,v3):
            self.assertEqual(round(math.sqrt(v*v),6),1) # checks to make sure normalized vectors have magnitude 1

        self.assertEqual(round(v1*v2,6),0)  # checks for orthogonality (rounds to avoid computing imperfections)
        self.assertEqual(round(v2*v3,6),0)
        self.assertEqual(round(v1*v3,6),0)

        # Test 2

        v4 = vector.V(5.7,0,-0.8)
        v5 = vector.V(0,-2,20)
        v6 = vector.V(7,-3,-9)

        v4.gram_schmidt(v5,v6)

        for v in (v4,v5,v6):
            self.assertEqual(round(math.sqrt(v*v),6),1)

        self.assertEqual(round(v4*v5,6),0)
        self.assertEqual(round(v5*v6,6),0)
        self.assertEqual(round(v4*v6,6),0)

        # Test 3

        v7 = vector.V(-2.2,-1,0.3)
        v8 = vector.V(19,-6,13)
        v9 = vector.V(85,-101,-43)

        v7.gram_schmidt(v8,v9)

        for v in (v7,v8,v9):
            self.assertEqual(round(math.sqrt(v*v),6),1)

        self.assertEqual(round(v7*v8,6),0)
        self.assertEqual(round(v8*v9,6),0)
        self.assertEqual(round(v7*v9,6),0)

                             
if __name__ == '__main__':
    unittest.main()
