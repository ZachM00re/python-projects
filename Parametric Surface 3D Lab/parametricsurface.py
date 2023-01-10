from functions import *
from vector import V
from gradient import Gradient
from polygon import Polygon


def lerp(x, a, b, c, d):
    return ((x-a)/(b-a))*(d-c) + c


class ParametricSurface():
    def __init__(self, func, n):
        self.func = func.function
        self.n = n
        self.xrange = func.xrange
        self.yrange = func.yrange
        self.zrange = func.zrange
        self.gradient = Gradient(func.zrange)
        self.makeHeightfield()


    def makeHeightfield(self):
        """calculate nxn 3d points in xrange x yrange
           store V(x,y,z) in self.heightfield[i,j]"""
        n = self.n
        self.heightfield = dict()
        xmin,xmax = self.xrange
        
        ymin,ymax = self.yrange

        for i in range(n):
            x = lerp(i,0,n-1,xmin,xmax)
            for j in range(self.n):
                y = lerp(j,0,n-1,ymin,ymax)
                pt = self.func(x,y)
                self.heightfield[i,j] = pt


    def projectPoints(self, eye):
        """project 3d points in heightfield to
              2d points (x,y) in plane of camera
              store in self.points[i,j]
           also calculate for these points
              self.minx, maxx, miny, maxy
           also calculate color based on gradient and height and normal
              store in self.color[i,j]
           also calculate eye distance
              store in self.distance[i,j]
        """

        fwd = -eye
        up = V(0,0,1)
        rt = fwd.cross(up)
        fwd.gram_schmidt(up,rt)

        self.points = dict()
        self.distance = dict()
        self.color = dict()

        n = self.n
        xmin = 1e10
        xmax = -1e10
        ymin = 1e10
        ymax = -1e10

        for i in range(n):
            for j in range(n):
                pt = self.heightfield[i,j]
                
                x = (pt - eye) * rt
                y = (pt - eye) * up
                
                d = (pt - eye).length()
                
                self.points[i,j] = (x/d,y/d) # to add perspective, makes farther polygons smaller
                
                self.distance[i,j] = d

                xmin = min(xmin,x/d)
                xmax = max(xmax,x/d)

                ymin = min(ymin,y/d)
                ymax = max(ymax,y/d)


                # Gathering 3 points from heightfield to derive two tangent vectors to surface
                
                if i == n-1:  
                    if j == n-1:
                        p0 = self.heightfield[i-1,j-1]
                        p1 = self.heightfield[i,j-1]
                        p2 = self.heightfield[i-1,j]
                    else:  
                        p0 = self.heightfield[i-1,j]
                        p1 = self.heightfield[i,j]
                        p2 = self.heightfield[i-1,j+1]
                elif j == n-1:
                    p0 = self.heightfield[i,j-1]
                    p1 = self.heightfield[i+1,j-1]
                    p2 = self.heightfield[i,j]
                    
                else:  
                    p0 = self.heightfield[i,j]
                    p1 = self.heightfield[i+1,j]
                    p2 = self.heightfield[i,j+1]

                v1 = p1-p0
                v2 = p2-p0


                # Determining shading using light vector and vector normal to parametric surface
                
                normal = v1.cross(v2)
                normal.normalize()

                light = V(2,-1,4)
                light.normalize()

                shade = max(0.25,normal * light)

                # Coloring based on height (z-coordinate)
                
                grad = Gradient(self.zrange)
                self.color[i,j] = grad.color(pt.z,shade)
                

        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax

    
    def scale(self,size):
        width,height = size

        xmin,xmax = self.xmin,self.xmax
        ymin,ymax = self.ymin,self.ymax
        n = self.n

        for i in range(n):
            for j in range(n):
                x,y = self.points[i,j]
                x = lerp(x,xmin,xmax,10,width-10)
                y = lerp(y,ymin,ymax,height-10,10)
                self.points[i,j] = x,y
                
        
    def makePolygons(self, eye, size):
        """project the points with self.projectPoints(eye)
           then build polygons from self.points, self.color, self.distance
           using [i,j], [i+1,j], [i+1,j+1], [i,j+1] indices
           then sort the polygons based on distance (farthest first)
        """

        polys = []
        newPolys = [] # will be returned as sorted polygon list
        distList = [] # added to help sort polygon instances

        self.projectPoints(eye)
        self.scale(size)
        
        n = self.n
        pts = self.points
        d = self.distance
        iteration = 0

        
        for i in range(n-1):
            for j in range(n-1):

                # Defining polygons with 4 points
                
                p1 = pts[i,j]
                color1 = self.color[i,j]
                d1 = d[i,j]
                
                
                p2 = pts[i+1,j]
                color2 = self.color[i+1,j]
                d2 = d[i+1,j]
                
                p3 = pts[i+1,j+1]
                color3 = self.color[i+1,j+1]
                d3 = d[i+1,j+1]
                
                p4 = pts[i,j+1]
                color4 = self.color[i,j+1]
                d4 = d[i,j+1]

                avgDist = (d1+d2+d3+d4)/4
                distList.append(avgDist) # makes a list with average distances of each polygon's points relative to eye

                p = Polygon([p1,p2,p3,p4],color1,avgDist)  # sets polygon color to color of p1
                polys.append(p)  # makes a list with all polygon instances


        distList.sort(reverse=True) # sorts average distances from large to small

        for item in distList:  # builds polygon list to match order of sorted list of distance attributes
            for poly in polys:
                if item == poly.distance:
                    newPolys.append(poly)
                    polys.remove(poly) # in case multiple polygons have same average, won't skip any or double count
                    break
                    
                    
        self.polygons = newPolys

 
