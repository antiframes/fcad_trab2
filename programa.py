import copy

import sys
import parser
import programa2

import numpy
from numpy import array
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import spsolve

import math
import cairo

WIDTH, HEIGHT = 1000, 1000

def main(argv):
	c1 = open(argv[0], 'r')
	net1 = parser.Parser(c1)

	#ASSIGNMENT - dividir em dois lados
	#passo 1: detectar a mediana
	aux = net1.Ax
	aux = numpy.sort(aux)
	sz  = len(aux)
	if sz%2 == 0:
		med = (aux[int(sz/2)-1] + aux[int(sz/2)])/2
	else:
		med = aux[int(sz/2)]
	#passo 2: dividir em dois grupos
	lefts=[]
	padsLeft=[]

	for x in range(len(net1.Ax)):
		if net1.Ax[x]>=med:
			lefts.append(False)
		else:
			lefts.append(True)
			
	for x in net1.pads:
		if int(x[2])*0.01> .5:
			padsLeft.append(False)
		else:
			padsLeft.append(True)

	gates_left = []
	gates_right = []
	for i in range(sz):
		if (lefts[i]==True):
			gates_left.append(i)		
		else:
			gates_right.append(i)
	plotarImage(net1.pads, net1.Bx , net1.By , net1.Ax , net1.Ay,"QP1")	

	#2QP - Posicionar os da esquerda
	pad_left = []
	C_left = []
	A_left = []
	Bx_left = []
	By_left = []
	Ax_left = []
	Ay_left = []

	#Bx By left
	szleft = len(gates_left)
	Bx_left = numpy.zeros( szleft, dtype=numpy.float_ )
	By_left = numpy.zeros( szleft, dtype=numpy.float_ )

	#Criar C left
	C_left = numpy.zeros( (szleft, szleft ) )
	diagonalAux = numpy.zeros( szleft )
	for i in range(szleft):
			aux_conn_gates = net1.conectadoAoGates(gates_left[i]) #confere se são vizinhos na A			
			for j in aux_conn_gates:
				entrou=0
				for k in range(szleft):#Busca o vizinho para fazer a ligação na nova C
					if gates_left[k] == j:
						C_left[k][i] = 1
						C_left[i][k] = 1	
						entrou =1

				if entrou==0:		# caso não encontrou nos vizinhos C, então é um pad
					Bx_left[i] += 50					  #addPadGate PSEUDO
					By_left[i] += net1.By[int(j)]	  #addPadGate PSEUDO
					diagonalAux[i] = diagonalAux[i]+1 #addPadGate PSEUDO

	#Criar A left
	diagonalA = C_left.sum(axis=0)
	diagonalA = diagonalA+diagonalAux
	A_left = C_left-(C_left+C_left)
	for n in range( len(gates_left)):
		A_left[n][n] = diagonalA[n]

	#adiciona se necessario os Pads aos By Bx (Pads Originais) 
	for n in net1.pads:
		retorno = net1.netConectaGates(n[1])
		for x in retorno:
			for k in range(len(gates_left)):
				if gates_left[k] == x: #Gate está na esquerda
					A_left[k][k]=A_left[k][k]+1 #Soma o pad na matriz A esquerda
					#Coneta ao Pad
					By_left[k] += float(n[3])		# Manter o Y sempre
					if padsLeft[int(n[0])-1] == True: # Se está na Esquerda
						Bx_left[k] += float(n[2])	#Mantem o memso X
					else:
						Bx_left[k] += 50			#Senão troca o x para 50

	#Ax Ay left	
	Ax_left = numpy.linalg.solve(A_left, Bx_left)
	Ay_left = numpy.linalg.solve(A_left, By_left) 
	
	#Copia Para Imprimir Pads
	newPadsLeft = copy.deepcopy(net1.pads)
	for n in range(len(newPadsLeft)):	
		if int(newPadsLeft[n][2])>50:
			newPadsLeft[n][2] = 50
	#FIM QP2

	#Propagar resultado para A original
	for k in range(len(gates_left)):
		net1.Ax[gates_left[k]] = Ax_left[k]
		net1.Ay[gates_left[k]] = Ay_left[k]
	
	#3QP - Posicionar os da Direita
	pad_right = []
	C_right = []
	A_right = []
	Bx_right = []
	By_right = []
	Ax_right = []
	Ay_right = []

	#Bx By right
	szright = len(gates_right)
	Bx_right = numpy.zeros( szright, dtype=numpy.float_ )
	By_right = numpy.zeros( szright, dtype=numpy.float_ )

	#Criar C right
	C_right = numpy.zeros( (szright, szright ) )
	diagonalAux = numpy.zeros( szright )
	for i in range(szright):
			aux_conn_gates = net1.conectadoAoGates(gates_right[i]) #confere se são vizinhos na A			
			for j in aux_conn_gates:
				entrou=0
				for k in range(szright):#Busca o vizinho para fazer a ligação na nova C
					if gates_right[k] == j:
						C_right[k][i] = 1
						C_right[i][k] = 1	
						entrou =1

				if entrou==0:		# caso não encontrou nos vizinhos C, então é um pad
					Bx_right[i] += 50				  #addPadGate PSEUDO
					By_right[i] += net1.By[int(j)]	  #addPadGate PSEUDO
					diagonalAux[i] = diagonalAux[i]+1 #addPadGate PSEUDO

	#Criar A right
	diagonalA = C_right.sum(axis=0)
	diagonalA = diagonalA+diagonalAux
	A_right = C_right-(C_right+C_right)
	for n in range( len(gates_right)):
		A_right[n][n] = diagonalA[n]

	#adiciona se necessario os Pads aos By Bx (Pads Originais) 
	for n in net1.pads:
		retorno = net1.netConectaGates(n[1])
		for x in retorno:
			for k in range(len(gates_right)):
				if gates_right[k] == x: #Gate está na direita
					A_right[k][k]=A_right[k][k]+1 #Soma o pad na matriz A esquerda
					#Coneta ao Pad
					By_right[k] += float(n[3])		# Manter o Y sempre
					if padsLeft[int(n[0])-1] == False: # Se está na Direita
						Bx_right[k] += float(n[2])	#Mantem o memso X
					else:
						Bx_right[k] += 50			#Senão troca o x para 50
	
	#Ax Ay right	
	Ax_right = numpy.linalg.solve(A_right, Bx_right)
	Ay_right = numpy.linalg.solve(A_right, By_right) 

	newPadsright = copy.deepcopy(net1.pads)
	for n in range(len(newPadsright)):	
		if int(newPadsright[n][2])<50:
			newPadsright[n][2] = 50
	#FIM QP3

	for k in range(len(gates_right)):
		net1.Ax[gates_right[k]] = Ax_right[k]
		net1.Ay[gates_right[k]] = Ay_right[k]

	plotarImage(newPadsLeft, Bx_left , By_left , Ax_left , Ay_left ,"QP2")
	plotarImage(newPadsright, Bx_right , By_right , Ax_right , Ay_right ,"QP3")		
	plotarImage(net1.pads, net1.Bx , net1.By , net1.Ax , net1.Ay,"Final")	
	
	nomeOut = "saida"
	out = open(nomeOut, 'w') 
	for k in range(len(net1.Ax)):
		soma = k+1
		
		string = str(soma) + " " + "%.8f" % net1.Ax[k] +" "+  "%.8f" % net1.Ay[k] +"\n"
		out.writelines(string ) 
	out.close()
	
def plotarImage(pads, Bx, By, Ax, Ay,name):
	#EXPORTAR IMAGEM
	surface = cairo.ImageSurface (cairo.FORMAT_ARGB32, WIDTH, HEIGHT)

	ctx = cairo.Context (surface)
	ctx.scale (WIDTH, HEIGHT) # Normalizing the canvas
	pat = cairo.LinearGradient (0.0, 0.0, 0.0, 1.0)
	pat.add_color_stop_rgba (1, 0.5, 0.5, 1, 1)
	ctx.rectangle (0, 0, 1, 1) # Rectangle(x0, y0, x1, y1)
	ctx.set_source (pat)
	ctx.fill ()
	ctx.set_source_rgb (0.3, 0.2, 0.5) # Solid color
	ctx.set_line_width (0.02)

	#Gates
	ctx.set_source_rgb (0.3, 0.2, 0.5)
	for i in range(len(Ax)):
		ctx.rectangle(Ax[i]*0.01,Ay[i]*0.01,0.01,0.01)
		ctx.close_path()
		ctx.stroke()

	#Pads
	ctx.set_source_rgb (0.5, 0.0, 0.0)
	for i in range(len(By)):
		if (int(By[i])==0 and int(Bx[i])==0):
			pass
		else:
			ctx.rectangle(Bx[i]*0.01,By[i]*0.01,0.01,0.01)
			ctx.close_path()
			ctx.stroke()
	ctx.set_source_rgb (0.0, 0.0, 0.0)
	for i in pads:
		ctx.rectangle(int(i[2])*0.01,int(i[3])*0.01,0.01,0.01)
		ctx.close_path()
		ctx.stroke()

	surface.write_to_png (name) # Output to PNG
    
if __name__ == "__main__":	
	main(sys.argv[1:])
