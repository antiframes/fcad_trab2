import sys
import parser
import programa2

import numpy
from numpy import array
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import spsolve

def main(argv):
	c1 = open(argv[0], 'r')
	net1 = parser.Parser(c1)
	print net1.Ax
	print net1.Ay
		
	
if __name__ == "__main__":	
	main(sys.argv[1:])
