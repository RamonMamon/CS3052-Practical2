import sys
import copy
from reduction_modules import Literal
from reduction_modules import Clause
from reduction_modules import Edge
from reduction_modules import Node

def read_initial():

    # implement a method of reading a command line argument which specifies
    # the type of operation that is going to be conducted.
    # This allows me to implement everything in just one file but also
    # allows me to create multiple executibles using a makefile with different args

    try:
        output_format = ''
        num_nodes = 0
        num_edges = 0

        while True:
            line = sys.stdin.readline().rstrip()
            line_val = line.split()

            if len(line_val) == 0:
                continue
            else:
                linetype = line_val[0]

            if linetype == 'p':
                output_format = line_val[1]
                num_nodes = int(line_val[2])
                num_edges = int(line_val[3])
                break
            elif linetype != 'c':
                raise ValueError

        while True:
            line = sys.stdin.readline().rstrip()
            line_val = line.split()

            if len(line_val) == 0:
                continue
            else:
                linetype = line_val[0]

            if linetype == 'colours':
                if len(line_val) > 2:
                    raise ValueError
                k = int(line_val[1])
                
                to_cnf(k, num_nodes, num_edges)
                # for edge in edges:
                #     print (' '.join(edge))
                break
            elif linetype != 'c':
                raise ValueError
    except ValueError:
        print('Invalid Format')
        exit(1)


# Converts a DIMACS COL format and transforms it into its equivalent SAT format and prints it out in the form DIMACS CNF
def to_cnf(k, num_nodes, num_edges):
    # kCol is a graph with k number of colors.

    nodes = []
    edges = []
    # p edge num_nodes num_edges
    # colours k for the k-colouring problem.
    # line = sys.stdin.readline().rstrip()
    for line in sys.stdin:

        line_vars = line.rstrip().split()
        line_type = line_vars[0]
        if line_type == 'e':
            # Edge values
            # e W V
            # Store mappings for each edge (W, V)
            if len(nodes) > num_nodes:
                raise ValueError
            if len(line_vars) != 3:
                raise ValueError

            node_w = Node(int(line_vars[1]))
            node_v = Node(int(line_vars[2]))
            if node_w not in nodes:
                nodes.append(node_w)
            else:
                # Uses the existing node instead
                node_w = next((x for x in nodes if x.value == node_w.value), node_w)

            if node_v not in nodes:
                nodes.append(node_v)
            else:
                # Uses the existing node instead
                node_v = next((x for x in nodes if x.value == node_v.value), node_v)

            edge = Edge(node_w, node_v)
            
            if edge in edges:
                raise ValueError
            
            

            edges.append(edge)
        elif line_type != 'c':
            # Ignores comments
            raise ValueError
        # Number of output Variables = Number of colors * number of nodes

    if len(edges) != num_edges or len(nodes) != num_nodes:
        raise ValueError
    
    num_variables = k * num_nodes
    num_lines = num_variables + (num_edges * k) + num_nodes
    color_index = 1
    print 'p cnf ' + str(num_variables) + ' ' + str(num_lines)

    for node in nodes:
        # Prints the color values for each node
        for i in range(0, k):
            # Distributes unique color values for each node
            color_value = (i*k) + color_index
            node.add_color(color_value)
        print str(node) + '0'
        
        color_index += 1

    # # TODO Print out At most One
    for node in nodes:
        for clause in node.amo_clauses():
            print str(clause) + '0'

    # TODO Print out Edge clauses
    for edge in edges:
        for clause in edge.color_clauses():
            print str(clause) + '0'
    

    # Comments are allowed anywhere
    # Ignore all descriptors in section 2.1 
    # Duplicate edges not allowed
    # An edge must be all on line
    # An edge is considered the same whichever order the nodes are listed
    # The duplicate ban means you can't have both edges 2-3 and 3-2
    # For 3-Col the number of colours is required to be exactly 3.
    

read_initial()