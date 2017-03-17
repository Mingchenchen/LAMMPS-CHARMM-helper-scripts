import sys
import math
import argparse

# Arg
def main(o, b, out):
    atoms_converted = {}

    # Find bond combinations that are necessary
    print "Looking for necessary bonds..."
    
    lines = o.readlines()
    bonds_necessary = {}
    foundbonds = False
    for l in lines:
        if not foundbonds:
            if l.find("# Bond Coeffs"):
                foundbonds = True
                continue
            else:
                continue
        
        parsed = l.split(' ')
        parsed = [x for x in parsed if x != '']
        if parsed[0] == '#':
            bond = parsed[2].split('-')
            bond[1] = bond[1].replace('\n','')
            bond[1] = bond[1].replace('\r','')
            bonds_necessary[(bond[0], bond[1])] = parsed[1]
        else:
            break
    print bonds_necessary
        
    # Finding bonds
    print "Finding bonds in bonds file..."
    
    lines = [line.rstrip('\n') for line in b]
    for l in lines:
        parsed = l.split("!")
        parsed = [x for x in parsed if x != '']
        commentary = parsed[1]
        parsed = parsed[0].split(" ")
        parsed = [x for x in parsed if x != '']
        print parsed
        
        index = bonds_necessary.get((parsed[0], parsed[1]), False) or bonds_necessary.get((parsed[1], parsed[0]), False)
        
        if index:
            string = "bond_coeff  "+ index+ "  "+ parsed[2]+ "  "+ parsed[3]+ " "+ "#" + commentary
            out.write(string)

    print "Done!"

# Run main
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Formata as combinacoes de bond coeff para script CHARMM.')

    parser.add_argument('original', metavar='txt', type=file, help='Arquivo original.')
    parser.add_argument('bonds', metavar='txt', type=file, help='Arquivo com os bonds.')
    parser.add_argument('output', metavar='txt', type=argparse.FileType('w'), help='Output convertido.')
    
    args = parser.parse_args()

    main(args.original, args.bonds, args.output)
