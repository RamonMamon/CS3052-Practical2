import sys
from reduction_modules import Literal
from reduction_modules import Clause
from reduction_modules import Edge
from reduction_modules import Node

def to_kCol(num_vars, num_clauses, input_source, output_file):

    # Must be positive
    variables = Clause()
    clauses = []

    for line in input_source:
        # Stores each clause 
        line_vars = line.strip().split()
        if len(line_vars) == 0:
            continue
            # break

        clause = Clause([i for i in line_vars if i != '0'])

        for i in line_vars:

            literal = Literal(i)

            # Checks if the variable is less than the number of variables.
            assert literal.get_variable() <= num_vars

            # Inserts the variable if it is unique
            if not variables.contains_literal(literal) and i != '0':
                variables.insert_literal(literal)
            
        clauses.append(clause) 
        
        assert len(clause) <= 3
        assert line_vars[0] != 'c'

    assert len(clauses) == num_clauses
    if len (variables) != 0:
        num_vars += 1

    while len(variables) < 4:
        # Makes the number of variables at least 4
        variables.insert_literal(Literal(str(num_vars)))
        num_vars += 1
    
    num_vars = len(variables)
    colour_index = num_vars * 2 + 1
    clause_index = num_vars * 3 + 1

    negation_variables = [str(i) for i in range(num_vars + 1, colour_index)]
    
    # Sets the colour indeces
    colours = [str(i) for i in range(colour_index, clause_index)]
    clause_variables = []
    edges = []

    for i in range(num_clauses):
        # Connect each Clause C to x and -x not in its clause

        clause_variable = clause_index + i

        for j in range(num_vars):
            
            variable_literal = variables.get_literal(j)
            if variable_literal not in clauses[i].literals:
                # Appends the edges created by x and -x when connected to the clause

                clause_node = Node(str(clause_variable))
                variable = str(variable_literal.get_variable())
                
                edges.append(Edge(Node(variable), clause_node))
                edges.append(Edge(Node(negation_variables[j]), clause_node))

        clause_variables.append(clause_variable)

    for i in range(num_vars):
        # Connect x to -x and both to the colour y

        variable_literal = variables.get_literal(i)
        variable = str(variable_literal.get_variable())

        x = Node(variable)
        x_negation = Node (negation_variables[i])
        edges.append(Edge(x, x_negation))

        for j in range(len(colours)):
            # Connect x and -x to y if i != j

            y = Node(colours[j])

            if j != i:
                edges.append(Edge(x, y))
                edges.append(Edge(x_negation, y))

    for colour_i in colours:
        # Connects colours to each other to make edges

        y_i = Node(colour_i)

        for colour_j in colours:

            if colour_i == colour_j:
                continue
            y_j = Node(colour_j)
            edge = Edge(y_i, y_j)

            if edge not in edges:
                edges.append(edge)

        
    # print("Variables")
    # for i in range(num_vars):
    #     variable_literal = variables.get_literal(i)
    #     variable = str(variable_literal.get_variable())

    #     print (variable)
    # print ("Negations")
    # for variable in negation_variables:
    #     print (variable)
    # print ("Colours")
    # for colour in colours:
    #     print (colour)
    # print ("Clauses")
    # for clause in clause_variables:
    #     print (clause)
    
    # Calculate number of nodes
    num_nodes = (3 * num_vars) + num_clauses
    print ('p edge', num_nodes, len(edges), file = output_file)
    print ('colours', len(colours) + 1, file = output_file)
    for edge in edges:
        print (edge, file = output_file)