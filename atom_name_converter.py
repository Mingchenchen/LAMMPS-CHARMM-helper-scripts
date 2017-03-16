import sys
import math
import argparse

# Arg
def main(o, c, out):
    atoms_converted = {}

    # First create the conversion for each atom on converter
    print "Reading converter..."

    base_state = ""
    lines = c.readlines()
    for l in lines:
        parsed = l.split(" ")
        parsed = [x for x in parsed if x != '']
        # Change base and create dictionary entry for base
        if parsed[0] == 'RESI':
            base_state = parsed[1]
            atoms_converted[base_state] = {}
            print "Base: ", base_state
            continue

        # Create dictionary entry inside a base state
        if parsed[0] == 'ATOM' and not atoms_converted[base_state].has_key(parsed[1]):
            parsed[3] = parsed[3].replace("\r", "")
            atoms_converted[base_state][parsed[1]] = [parsed[2], parsed[3].replace('\n', '')]
    print "Done reading!"

    print "Conversion will be: "
    print atoms_converted
    
    # Converting original file
    print "Converting original file..."
    lines = [line.rstrip('\n') for line in o]
    for l in lines:
        parsed = l.split(" ")
        parsed = [x for x in parsed if x != '']
        base_state = ""
        # Check base!
        if len(parsed) == 12:
            if parsed[3] == "A":
                base_state = "ADE"
            elif parsed[3] == "T":
                base_state = "THY"
            elif parsed[3] == "C":
                base_state = "CYT"
            elif parsed[3] == "G":
                base_state = "GUA"
            else:
                print "ERROR: don't know which base is ", parsed[7] 
                continue
        else:
            continue
        
        if atoms_converted[base_state].has_key(parsed[2]):
            index = parsed[2]
            
            # Change name
            conversion_name = atoms_converted[base_state][index][0]
            size = len(parsed[2]) - len(conversion_name)
            if size < 0:
                for i in range(0, -size):
                    parsed[2] += " "
            elif size > 0:
                for i in range(0, size):
                    conversion_name += " "
            l = l.replace(parsed[2], conversion_name)

            # Change charge
            conversion_charge = atoms_converted[base_state][index][1]
            size = len(parsed[10]) - len(conversion_charge)
            if size < 0:
                for i in range(0, -size):
                    parsed[10] += " "
            elif size > 0:
                for i in range(0, size):
                    conversion_charge += " "
            l = l.replace(" " + parsed[10], " " + conversion_charge + " ")
            
        # Output
        out.write(l + "\n")
    print "Done!"

# Run main
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Converte o nome dos atomos.')

    parser.add_argument('original', metavar='txt', type=file, help='Arquivo original.')
    parser.add_argument('conversor', metavar='txt', type=file, help='Arquivo com a conversao.')
    parser.add_argument('output', metavar='txt', type=argparse.FileType('w'), help='Output convertido.')
    
    args = parser.parse_args()

    main(args.original, args.conversor, args.output)
