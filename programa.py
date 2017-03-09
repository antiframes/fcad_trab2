import numpy
from numpy import array
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import spsolve

class Point:
    def __init__(self):
        self.connections=[]
        self.pads=[]
    def insertConnection(self,connection):
        self.connections.append(connection)
    def insertPad(self,pad):
        self.pads.append(pad)
class Pad:
    def __init__(self,x,y):
        self.x=x
        self.y=y

pads = []
pads.append(Pad(0,1))
pads.append(Pad(1,1))
pads.append(Pad(1,0))
pads.append(Pad(0.5,0))

points = []
points.append(Point())
points.append(Point())
points.append(Point())
points.append(Point())
points.append(Point())

points[0].insertConnection(1)
points[0].insertConnection(2)
points[0].insertPad(0)


points[1].insertConnection(0)
points[1].insertConnection(2)
points[1].insertConnection(3)
points[1].insertConnection(4)


points[2].insertConnection(0)
points[2].insertConnection(1)
points[2].insertConnection(3)
points[2].insertPad(2)


points[3].insertConnection(1)
points[3].insertConnection(2)
points[3].insertConnection(4)
points[3].insertPad(1)


points[4].insertConnection(1)
points[4].insertConnection(3)
points[4].insertPad(3)
