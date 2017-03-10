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
		self.generate(file)
		self.criarC()

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
				

	
			
