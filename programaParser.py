import sys
import parser
import programa2

def main(argv):
	c1 = open(argv[0], 'r')
	net1 = parser.Parser(c1)
	print net1.A
#	print net1.C
#	for i in net1.pads:
		#print i
		#print net1.netConectaGates(i[1])
		
	
if __name__ == "__main__":	
	main(sys.argv[1:])
