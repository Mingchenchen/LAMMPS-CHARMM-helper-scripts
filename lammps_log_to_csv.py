import sys
import math
import argparse

# Arg
def main(o, out):

    # Read the lines
    print "Reading log..."

    lines = o.readlines()
    parsed_lines = []
	
    for l in lines:
        parsed = l.split(" ")
        parsed = [x for x in parsed if x != ' ']
        parsed = [x for x in parsed if x != '']
        parsed = [x for x in parsed if x != '\r\n']
        parsed_lines.append(parsed)
	
    print "Done reading!"

    # Converting file
    print "Converting file..."
    
    for l in parsed_lines:
        new_line = ""
        for s in l:
            new_line = new_line + s + ','
        
        # Output
        out.write(new_line + "\n")
    print "Done!"

# Run main
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Converte o log do LAMMPS em uma tabela CSV.')

    parser.add_argument('original', metavar='txt', type=file, help='Log do LAMMPS.')
    parser.add_argument('output', metavar='txt', type=argparse.FileType('w'), help='Output convertido.')
    
    args = parser.parse_args()

    main(args.original, args.output)
