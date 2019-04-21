import sys
from reduction_modules import Literal
from reduction_modules import Clause


    # Make a to_string function
def read_initial():

    # implement a method of reading a command line argument which specifies
    # the type of operation that is going to be conducted.
    # This allows me to implement everything in just one file but also
    # allows me to create multiple executibles using a makefile with different args
    output = []
    output_format = ''
    num_lines = 0
    num_vars = 0
    try:
        # tempLime = sys.stdin.read()

        # print (tempLime)
        while True:
            line = sys.stdin.readline().rstrip()
            line_val = line.split()
            # print (line)
            if len(line_val) == 0:
                continue

            linetype = line[0]

            if linetype == 'p':
                # If output format is cnf then use to_sat3 
                # else use to_cnf
                output_format = line_val[1]
                if output_format != 'cnf':
                    raise ValueError
                num_vars = int(line_val[2])
                num_lines = int(line_val[3])
                to_sat3(num_vars, num_lines, output)
                break
            elif linetype != 'c':
                raise ValueError
    except ValueError:
        print('Invalid Format')
        exit(1)

def to_sat3(num_vars, num_lines, output):

    # Read SAT in CNF from stdin
    # Check the first character of every line
    variables = []
    clauses = []
    new_var_index = num_vars + 1
    
    for line in sys.stdin:
        # Stores each clause 
        line_vars = line.strip().split()
        if len(line_vars) == 0:
            break
        clauses.append(line_vars)
        if len(clauses) > num_lines:
            raise ValueError
    
    for line in clauses:
        # Parses each line 
        literal_index = 0
        clause = Clause()      
        while True:
            if len(line) == 0:
                break
            
            # Gets the character at the first index
            literal = Literal(line.pop(0))
            
            # Check each character and see if it's already saved
            if literal.value() != 0 and literal not in variables:
                variables.append(literal)

            # Check if the number of variables is greater than num_vars
            if len(variables) > num_vars:
                raise ValueError
            
            if literal.value() == 0:
                # Creates a new clause when the literal is 0
                clause.insert_literal(literal)
                output.append(clause)
                clause = Clause()
                literal_index = 0

            elif literal_index % 3 == 0 and literal_index != 0:
                # Splits the clauses if the number of clauses is greater than 3

                # Returns the third and fourth literals to the beginning of the list of Line literals
                third = str(literal)
                fourth = str(clause.pop())

                line.insert(0, third)
                line.insert(0, fourth)

                var_string = str(new_var_index)
                new_variable = Literal(var_string)
                clause.insert_literal(new_variable)
                clause.insert_literal(Literal('0'))

                line.insert(0,'-' + var_string)

                output.append(clause)
                clause = Clause()
                
                num_lines += 1
                num_vars += 1
                new_var_index += 1
                literal_index = 0

            else:
                # Appends the literal to the output_line
                clause.insert_literal(literal)
                if len(line) == 0:
                    clause.insert_literal(Literal('0'))
                    output.append(clause)
                literal_index += 1  

    if num_lines > len(output):
        raise ValueError

    print ('p cnf ' + str(len(variables)) + ' ' + str(len(output)))
    for clause in output:
        print(clause)

read_initial()
# for line in sys.stdin:
#     print (line.rstrip())
