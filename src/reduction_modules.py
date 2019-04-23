import copy

class Literal:
    """
    The distinction between value and variable for a Literal
    allows it to be used in contexts wherein a specific variable
    should not be repeated, but at the same time still allow its
    value to be stored.
    """
    def __init__(self, variable):
        self.state = True
        self.variable = 0

        assert '--' not in variable
        if variable[0] == '-':
            self.state = False
            self.variable = int(variable[1:])

        else:
            self.variable = int(variable)    

    # Returns the actual value of the Literal
    def value(self):
        if not self.state:
            return -1 * self.variable
        return self.variable

    # Returns variable without its sign
    def get_variable(self):
        return self.variable
        
    # Allows for the literal's state to be set
    def set_state(self, val):
        self.state = val

    def __str__(self):
        return str(self.value())

    def __eq__(self, that):
        if self.variable == that.variable:
            return True
        return False

        
class Clause:
    def __init__(self, literals = []):
        self.literals = []
        for val in literals:
            literal = Literal(val)
            self.literals.append(literal)

    # Appends the literal to the end of the list
    def insert_literal(self, literal):
        self.literals.append(literal)

    # Removes the literal at the index
    def remove_literal(self, literal):
        self.literals.remove(literal)

    # Returns the Literal at the index 
    def get_literal(self, index):
        return self.literals[index]

    # Pops the literal from the clause
    def pop(self, index = -1):
        return self.literals.pop(index)
    
    # Returns the unsigned variable of a literal
    def get_literal_variable(self, index):
        return self.literals[index].get_variable()

    # Returns the signed value of the literal
    def get_literal_value(self, index):
        return self.literals[index].value()

    # Checks the list of literals to see if a literal exists
    def contains_literal(self, literal):
        if literal in self.literals:
            return True
        return False

    # Checks if the Clause contains a value 
    def contains_value(self, value):
        # literal = Literal(value)
        for literal in self.literals:
            if value == literal.value():
                return True
        return False
        # return self.contains_literal(literal)

    # Returns a copy of the clause with only one value set to true
    def at_most_one(self, index):
        clause = Clause()
        for i in range(len(self.literals)):
            literal = copy.deepcopy(self.literals[i])
            if i != index:
                literal.set_state(False)
                clause.insert_literal(literal)
                
        return clause
    
    def __len__(self):
        return len(self.literals)

    def __str__(self):
        string = ''
        for literal in self.literals:
            string += str(literal) + ' '
        return string

class Edge:
    def __init__(self, w, v):
        self.w = w
        self.v = v

    # Returns a list of clauses that makes 1 literal true by making everything else false
    def color_clauses(self):
        clauses = []
        for i in range(0, len(self.w.color)):
            # Gets every edge clause possible from each node
            clause = Clause()

            literal1 = copy.deepcopy(self.w.get_color(i))
            literal2 = copy.deepcopy(self.v.get_color(i))

            # Change states of literals to negations
            literal1.set_state(False)
            literal2.set_state(False)

            clause.insert_literal(literal1)
            clause.insert_literal(literal2)
            clauses.append(clause)
        return clauses

    def __eq__(self, value):
        if self.w == value.w and self.v == value.v:
            return True
        elif self.w == value.v and self.v == value.w:
            return True
        return False

    def __str__(self):
        return 'e ' + str(self.w.get_value()) + ' ' + str(self.v.get_value())
        
class Node:
    def __init__(self, val):
        assert int(val) >= 1
        self.literal = Literal(val)
        self.color = Clause()

    # Adds a color to the node
    def add_color(self, val):
        color_literal = Literal(str(val))
        self.color.insert_literal(color_literal)

    # Returns a color of the node at a certain index
    def get_color(self, index):
        return self.color.get_literal(index)

    # Returns the number of colors contained in the node
    def num_colors(self):
        return len(self.color)

    # Returns the Clause that contains all the colors in the node.
    def get_colors(self):
        return self.color
        
    # Returns a list of clauses with all the possible at most one colours in each clause
    def amo_clauses(self):
        clauses = []
        length = self.num_colors()
        for i in range(0, length):
            clause = self.color.at_most_one(i)
            clauses.append(clause)
        return clauses

    # Returns the value of the node (Always positive)
    def get_value(self):
        return self.literal.variable

    def __eq__(self, that):
        if self.literal == that.literal:
            return True
        # TODO Perhaps add color checking in the future
        return False

    def __str__(self):
        return str(self.color)

    