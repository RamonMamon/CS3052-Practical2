import sys

class Literal:
    is_negative = False
    variable = 0
    def __init__(self, variable):
        if '--' in variable:
            raise ValueError
        elif variable[0] == '-':
            self.is_negative = True
        self.variable = int(variable[1:])

    def get_variable(self):
        if self.is_negative:
            return -variable
        return variable

    # Checks if the other literal has the same variable.
    def __eq__(self, that):
        if self.variable == that.variable:
            return True
        return False
        
        
class Clause:
    literals = []

    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs)

def read_initial():

    # implement a method of reading a command line argument which specifies
    # the type of operation that is going to be conducted.
    # This allows me to implement everything in just one file but also
    # allows me to create multiple executibles using a makefile with different args

    
    try:
        output_format = ''
        num_lines = 0
        num_vars = 0

        while True:
            line = sys.stdin.readline().rstrip()
            line_val = line.split()

            if len(line_val) == 0:
                continue
            else:
                linetype = line_val[0]

            if linetype == 'p':
                # If output format is cnf then use to_sat3 
                # else use to_cnf
                output_format = line_val[1]
                # if output_format == 'cnf':
                num_lines = int(line_val[2])
                num_vars = int(line_val[3])
                to_sat3(num_lines, num_vars)
                break
            elif linetype != 'c':
                raise ValueError
    except ValueError:
        print('Invalid Format')
        sys.exit(1)


def to_sat3(num_lines, num_vars):

    # Read SAT in CNF from stdin
    # Check the first character of every line
    output = []
    literals = []
    new_var_index = 1
    i = 0
    
    while True:
        if i > num_lines:
            raise ValueError    
        line = sys.stdin.readline().rstrip()
        line_vars = line.split()

        lit_index = 0
        output_line = []

        # Want to append characters to an output line

        while True:
            if len(line_vars) == 0:
                break
            literal = line_vars.pop(0)

            # Check each character and see if it's already saved

            if literal != '0' and literal not in literals:
                literals.append(literal)

            # Check if the number of variables is greater than num_vars

            if len(literals) > num_vars:
                raise ValueError

            # TODO check if the literals have a double negative.
            
            if literal == '0':

                # Creates a new line when the literal is 0

                output_line.append('0')
                output.append(output_line)
                output_line = []
                lit_index = 0
            elif lit_index % 3 == 0 and lit_index != 0:

                # Splits the clauses if the number of clauses is greater than 3

                # Returns the third and fourth index to the beginning of the list of Line literals

                line_vars.insert(0, literal)
                line_vars.insert(0, output_line.pop())

                newVar = 'y' + str(new_var_index)
                output_line.append(newVar)
                output_line.append('0')

                # Appends the negation of the new variable to the list of line literals

                line_vars.append('-' + newVar)
                output.append(output_line)
                output_line = []

                # Increment 1 to the number of vars to compensate for the newly added negative variable

                num_vars += 1
                new_var_index += 1
                lit_index = 0
            else:

                # Appends the literal to the output_line

                # Catches double negatives.
                if '--' in literal:
                    raise ValueError

                output_line.append(literal)
                if len(line_vars) == 0:
                    output_line.append('0')
                    output.append(output_line)
                lit_index += 1
        i += 1
    for line in output:
        print(' '.join(line))

read_initial()
