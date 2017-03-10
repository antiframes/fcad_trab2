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

class Parser:
	def __init__(self, file):
		self.nGates = 0
		self.nNet = 0
		self.nPad = 0
		self.pads = []	
		self.linhaPads = []
		self.points = []
		self.linhaGates = []
		self.generate(file)

	def generate(self, file):
		for line in file:
			list = line[0:line.find('#')].lower().split()
			self.nGates = list[0] #nGates
			self.nNet = list[1] #nNet
			print list[1]
			for n in xrange(0, int(self.nGates)):
				for line in file:	
					list=line[0:line.find('#')].lower().split()
					self.points.append(Point())
					self.linhaGates.append(list[2:]) 
					for g in list[2:]:
						self.points[n].insertConnection(int(g))	
					break

			for line in file:	
				list=line[0:line.find('#')].lower().split()
				self.nPad = list[0] #nPad
				break

			for n in xrange(0, int(self.nPad)):	
				for line in file:	
					list=line[0:line.find('#')].lower().split()
					self.linhaPads.append(list) 
					self.pads.append(Pad(list[2],list[3]))				
					break
