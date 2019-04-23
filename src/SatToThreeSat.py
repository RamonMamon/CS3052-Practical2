import sys
from reduction_modules import Literal
from reduction_modules import Clause

def to_sat3(num_vars, num_lines, input_source, output_file):

    # Read SAT in CNF from stdin
    # Check the first character of every line
    output = []
    variables = []
    clauses = []
    new_var_index = num_vars + 1
    
    for line in input_source:
        # Stores each clause 
        line_vars = line.strip().split()
        if len(line_vars) == 0:
            continue
        # clauses.append(Clause([i for i in line_vars ]))
        clauses.append(line_vars)
        assert len(clauses) <= num_lines
    
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
            assert len(variables) <= num_vars
            
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

    assert num_lines <= len(output)

    print ('p cnf ' + str(len(variables)) + ' ' + str(len(output)), file = output_file)
    for clause in output:
        print(clause, file = output_file)
