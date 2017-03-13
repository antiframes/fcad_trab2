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
	#print(net1.Ax)
	#print(net1.Ay)
	
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
	for x in range(len(net1.Ax)):
		if net1.Ax[x]>=med:
			lefts.append(False)
			if net1.Ax[x] < 50:
				net1.Ax[x] = 100-net1.Ax[x]
		else:
			lefts.append(True)
	#2QP - Posicionar os da esquerda
	left_gates_x=[]
	left_gates_y=[]
	for i in range(sz):
		if (lefts[i]==True):
			pass

	surface = cairo.ImageSurface (cairo.FORMAT_ARGB32, WIDTH, HEIGHT )
	ctx = cairo.Context (surface)
	ctx.scale (WIDTH, HEIGHT) # Normalizing the canvas
	pat = cairo.LinearGradient (0.0, 0.0, 0.0, 1.0)
	pat.add_color_stop_rgba (1, 0.5, 0.5, 1, 1)
	ctx.rectangle (0, 0, 1, 1) # Rectangle(x0, y0, x1, y1)
	ctx.set_source (pat)
	ctx.fill ()
	ctx.set_source_rgb (0.3, 0.2, 0.5) # Solid color
	ctx.set_line_width (0.02)
	for i in range(len(net1.Ax)):
		if lefts[i]==True:
			ctx.set_source_rgb (0.3, 0.2, 0.5)
		else:
			ctx.set_source_rgb (0.5, 0.3, 0.2)
		ctx.rectangle(net1.Ax[i]*0.01,net1.Ay[i]*0.01,0.01,0.01)
		ctx.close_path()
		ctx.stroke()

	surface.write_to_png ("plot.png") # Output to PNG
    
	
if __name__ == "__main__":	
	main(sys.argv[1:])
