import sys
from SatToThreeSat import to_sat3
from KColtoSat import to_cnf
from ThreeSatToCol import to_kCol

def parse():
    parse_type = sys.argv[1]

    try:
        input_source = sys.stdin
        output_file = sys.stdout
        
        # Reads input from file if specified
        if len(sys.argv) >= 3:
            input_source = open(sys.argv[2], 'r')
        
        # Print out to file if specified
        if len(sys.argv) >= 4:
            output_file = open(sys.argv[3], 'w')
        
        for line in input_source:
            line_val = line.rstrip().split()
            if len(line_val) == 0:
                continue
            linetype = line[0]

            # If the line is a comment, ignore
            if linetype == 'c':
                continue

            format_type = line_val[1]

            assert linetype == 'p'

            param1 = int(line_val[2])
            param2 = int(line_val[3])
            
            if parse_type == 'cnf':
                # Takes a cnf sat input and prints it out as sat3

                assert format_type == parse_type
                to_sat3(param1, param2, input_source, output_file)

            elif parse_type == '3sat':
                # Takes a cnf 3sat input and prints it out as kcol

                assert format_type == 'cnf'
                to_kCol(param1, param2, input_source, output_file)

            elif parse_type == 'edge':
                # Takes a kCol input and prints it out to sat

                assert format_type == parse_type
                to_cnf(param1, param2, input_source, output_file)

            else:
                raise ValueError

            break
    except (ValueError , AssertionError) as e:
        print('Invalid Format')
        exit(1)

parse()