import sys
import copy
from reduction_modules import Literal
from reduction_modules import Clause
from reduction_modules import Edge
from reduction_modules import Node

# Converts a DIMACS COL format and transforms it into its equivalent SAT format and prints it out in the form DIMACS CNF
def to_cnf(num_nodes, num_edges, input_source, output_file):
    nodes = []
    edges = []
    k = 0

    # Gets the number of colours
    for line in input_source:
        line_val = line.rstrip().split()

        if len(line_val) == 0:
            continue
        linetype = line_val[0]

        if linetype == 'c':
            continue

        assert linetype == 'colours'
        assert len(line_val) == 2
        k = int(line_val[1])
        break
        
    
    # Parses the input edges
    for line in input_source:
        line_vars = line.rstrip().split()
        line_type = line_vars[0]

        
        if line_type == 'c':
            continue
        
        # Store mappings for each edge (W, V)
        
        assert line_type == 'e'
        assert len(nodes) <= num_nodes
        assert len(line_vars) == 3
        
        node_w = Node(line_vars[1])
        node_v = Node(line_vars[2])

        # Uses the stored node if node already exists
        if node_w not in nodes:
            nodes.append(node_w)
        else:
            node_w = next((x for x in nodes if x.literal == node_w.literal), node_w)

        # Uses the stored node if node already exists
        if node_v not in nodes:
            nodes.append(node_v)
        else:
            node_v = next((x for x in nodes if x.literal == node_v.literal), node_v)

        edge = Edge(node_w, node_v)            
        assert edge not in edges
        edges.append(edge)

        # Number of output Variables = Number of colors * number of nodes

    assert len(edges) == num_edges 
    assert len(nodes) == num_nodes
    
    num_variables = k * num_nodes
    num_lines = num_variables + (num_edges * k) + num_nodes
    color_index = 1
    print ('p cnf ' + str(num_variables) + ' ' + str(num_lines), file = output_file)

    # Prints out At least one
    for node in nodes:
        # Prints the color values for each node
        for i in range(0, k):
            # Distributes unique color values for each node
            color_value = (i*k) + color_index
            node.add_color(color_value)
        print (str(node) + '0', file = output_file)
        
        color_index += 1

    # Print out At most One
    for node in nodes:
        for clause in node.amo_clauses():
            print (str(clause) + '0', file = output_file)

    # Print out Edge clauses
    for edge in edges:
        for clause in edge.color_clauses():
            print (str(clause) + '0', file = output_file)
