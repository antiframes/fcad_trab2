import numpy as np
import sys
class Parser:
	def __init__(self, file):
		self.nGates = 0
		self.nNet = 0
		self.nPad = 0
		self.gates = []
		self.pads = []
		self.conexao = []
		self.C = []
		self.A = []
		self.Ax = []
		self.Ay = []
		self.Bx = []
		self.By = []
		self.generate(file)
		self.criarC()
		self.criarA()
		self.criarB()
		self.criarAxAy()

	def generate(self, file):
		for line in file:
			list = line[0:line.find('#')].lower().split()
			self.nGates = list[0] #nGates
			self.nNet = list[1] #nNet
			self.conexao = np.zeros( (int(self.nNet),int(self.nGates)) )
			for n in xrange(0, int(self.nGates)):
				for line in file:	
					list=line[0:line.find('#')].lower().split()
					self.gates.append(list[2:]) 
					for g in list[2:]:
						self.conexao[int(g)-1][int(list[0])-1] = 1
					break

			for line in file:	
				list=line[0:line.find('#')].lower().split()
				self.nPad = list[0] #nPad
				break

			for n in xrange(0, int(self.nPad)):	
				for line in file:	
					list=line[0:line.find('#')].lower().split()
					self.pads.append(list) 
					break
	def criarAxAy(self):
		self.Ax = np.linalg.solve(self.A, self.Bx)
		self.Ay = np.linalg.solve(self.A, self.By) 
 
	def criarA(self):
		self.A = self.C-(self.C+self.C)
		diagonalA = self.C.sum(axis=0)
		for n in xrange(0, int(self.nGates)):
			self.A[n][n] = diagonalA[n]
		for i in self.pads:
			retorno = self.netConectaGates(i[1])
			for x in retorno:
				self.A[x][x]=self.A[x][x]+1

	def criarB(self):
		self.Bx = np.zeros( (int(self.nGates), 1) )
		self.By = np.zeros( (int(self.nGates), 1) )
		for i in self.pads:
			retorno = self.netConectaGates(i[1])
			for x in retorno:
				self.Bx[x]= i[2]
				self.By[x]= i[3]

	def criarC(self):
		self.C = np.zeros( (int(self.nGates),int(self.nGates)) )
		for i in self.conexao:
			vetorAux = []
			contadorj =0
			for j in i:
				if j==1:
					vetorAux.append(contadorj)
				contadorj=contadorj+1
			if len(vetorAux)>1:
				for k in vetorAux:
					if len(vetorAux)==1:
						break
					for lk in vetorAux[1:]:
						self.C[int(k)][int(lk)]=1
						self.C[int(lk)][int(k)]=1
					vetorAux=vetorAux[1:]

	def netConectaGates(self, nNet):
		retorno = []
		for n in xrange(0, int(self.nGates)):
			if self.conexao[int(nNet)-1][n]==1:
				retorno.append(n)
		return retorno
