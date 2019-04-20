import sys

class Edge:
    w = ''
    v = ''

    def __init__(self, w, v):
        if int(w) < 1 or int(v) < 1:
            raise ValueError
        self.w = w
        self.v = v

    def __eq__(self, value):
        
        if self.w == value.w and self.v == value.v:
            return True
        elif self.w == value.v and self.v == value.w:
            return True
        return False
        

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
                k = line_val[1]
                edges = []
                to_cnf(k, num_nodes, num_edges, edges)
                for edge in edges:
                    print (' '.join(edge))
                break
            elif linetype != 'c':
                raise ValueError
    except ValueError:
        print('Invalid Format')
        exit(1)


# Converts a DIMACS COL format and transforms it into its equivalent SAT format and prints it out in the form DIMACS CNF
def to_cnf(k, num_nodes, num_edges, edges):
    # kCol is a graph with k number of colors.
    '''
    For each node i in the graph, introduce k new SAT variables
        
        y(i,1), y(i,2), . . . y(i,k)

    Each variable y(i,j) will be true iff node i is coloured with colour j. We need three types of clauses.
        • ‘At-least-one’ clauses (ALO). A single clause {y(i,1), y(i,2), . . . y(i,k)} for each node i, which says that each node has
        to have at least one colour.
        • ‘At-most-one’ clauses (AMO). A clause for every node and pair j, j(prime) of colours. The clause {¬y(i,j) , ¬y(i,j0)} says
        that node i can’t be both colour j and colour j(prime).
        • ‘Edge’ clauses. For each edge in the graph connecting nodes i and i(prime), one clause for each colour j. The clause
        {¬y(i,j) , ¬y(i,j)} says that either i or i(prime) is not coloured with j (or neither is).
    '''

    # p edge num_nodes num_edges
    # colours k for the k-colouring problem.
    line = sys.stdin.readline().rstrip()
    line_vars = line.split()
    line_type = line_vars[0]
    edges = []
    if line_type == 'c':
        to_cnf(k, num_nodes, num_edges, edges)
    elif line_type == 'e':
        # Edge values
        # e W V
        # Store mappings for W, V 

        if len(line_vars) != 3:
            raise ValueError

        edge = Edge(line_vars[1], line_vars[2])
        
        if edge in edges:
            raise ValueError
        
        edges.append(edge)
        
        # Number of output Variables = Number of colors * number of nodes
    # Comments are allowed anywhere
    # Ignore all descriptors in section 2.1 
    # Duplicate edges not allowed
    # An edge must be all on line
    # An edge is considered the same whichever order the nodes are listed
    # The duplicate ban means you can't have both edges 2-3 and 3-2
    # For 3-Col the number of colours is required to be exactly 3.
    return

read_initial()