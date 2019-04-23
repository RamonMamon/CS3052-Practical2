import sys
from reduction_modules import Literal
from reduction_modules import Clause

def to_sat3(num_vars, num_lines, input_source, output_file):

    # Read SAT in CNF from stdin
    # Check the first character of every line
    clauses = []
    for line in input_source:
        # Stores each clause 
        line_vars = line.strip().split()
        if len(line_vars) == 0:
            continue
        clauses.append(Clause([i for i in line_vars]))
        # clauses.append(line_vars)
        assert len(clauses) <= num_lines

    output_clauses = []
    variables = []

    for clause in clauses:
        # Parses each line 
        literal_index = 0
        temp_clause = Clause()      

        for i in range(len(clause)):
            literal = clause.get_literal(i)

            # Checks if the literal value is less than the number of variables
            assert literal.get_variable() <= num_vars

            # Check each character and see if it's already saved
            if literal.value() != 0 and literal not in variables:
                variables.append(literal)

            # Check if the number of variables is greater than num_vars
            assert len(variables) <= num_vars

            if literal.value() == 0:
                # Creates a new clause when the literal is 0

                temp_clause.insert_literal(literal)
                output_clauses.append(temp_clause)
                temp_clause = Clause()

            elif len(temp_clause) == 3:
                # Creates a new clause that is connected by a new variable

                num_vars += 1
                num_lines += 1
                third_literal_value = str(temp_clause.pop())

                new_variable = Literal(str(num_vars))
                

                temp_clause.insert_literal(new_variable)
                temp_clause.insert_literal(Literal('0'))
                output_clauses.append(temp_clause)

                temp_clause = Clause([str(-num_vars), third_literal_value, str(literal) ])

            else:
                # Appends the literal to the clause.

                temp_clause.insert_literal(literal)

                if i == len(clause):
                    # Add a 0 literal to the end of the clause
                    
                    temp_clause.insert_literal('0')
                    output_clauses.append(temp_clause)

    assert num_lines <= len(output_clauses)

    print ('p cnf', num_vars, num_lines, file = output_file)
    for clause in output_clauses:
        print(clause, file = output_file)
