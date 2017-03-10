import sys
import parser
import programa2

def main(argv):
	c1 = open(argv[0], 'r')
	net1 = parser.Parser(c1)
	print net1.gates
	print net1.C
	print "teste2"
	c2 = open(argv[0], 'r')
	net2 = programa2.Parser(c2)
	
	print net2.points.

if __name__ == "__main__":	
	main(sys.argv[1:])
