import sys
import parser
import programa2

def main(argv):
	c1 = open(argv[0], 'r')
	net1 = parser.Parser(c1)
	print net1.A
		
	
if __name__ == "__main__":	
	main(sys.argv[1:])
