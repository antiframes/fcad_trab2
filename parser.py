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

	def conectadoAoPad(self, entrada):
		retorno=[]
		for i in self.pads:
			ret = self.netConectaGates(i[1])
			for k in ret:
				if k==entrada:	
					aux = int(i[0])
					retorno.append(aux-1)
		return retorno
			
	def conectadoAoGates(self, i):
		retorno = []
		for n in range(len(self.C[i])):
			if self.C[i][n]!=0:
				retorno.append(n)
		
		return retorno
		
	def generate(self, file):
		for line in file:
			list = line[0:line.find('#')].lower().split()
			self.nGates = list[0] #nGates
			self.nNet = list[1] #nNet
			self.conexao = np.zeros( (int(self.nNet),int(self.nGates)) )
			for n in range(int(self.nGates)):
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

			for n in range(int(self.nPad)):	
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
		for n in range(int(self.nGates)):
			self.A[n][n] = diagonalA[n]
		for i in self.pads:
			retorno = self.netConectaGates(i[1])
			for x in retorno:
				self.A[x][x]=self.A[x][x]+1

	def criarB(self):
		self.Bx = np.zeros( int(self.nGates), dtype=np.float_ )
		self.By = np.zeros( int(self.nGates), dtype=np.float_ )
		for i in self.pads:
			retorno = self.netConectaGates(i[1])
			for x in retorno:
				self.Bx[x] += float(i[2])
				self.By[x] += float(i[3])

	def criarC(self):
		self.C = np.zeros( (int(self.nGates),int(self.nGates)) )
		for i in self.conexao:
			vetorAux = []
			for j in range(len(i)):
				if i[j]==1:
					vetorAux.append(j)
			if len(vetorAux)>1:
				for k in range(len(vetorAux)):
					for lk in range(len(vetorAux)):
						if k!=lk:
							self.C[vetorAux[k]][vetorAux[lk]]=1
							self.C[vetorAux[lk]][vetorAux[k]]=1


	def netConectaGates(self, nNet):
		retorno = []
		for n in range(int(self.nGates)):
			if self.conexao[int(nNet)-1][n]==1:
				retorno.append(n)
		return retorno
