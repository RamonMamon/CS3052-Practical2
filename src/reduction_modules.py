import copy

class Literal:
    def __init__(self, variable):
        self.state = True
        self.variable = 0

        assert '--' not in variable
        if variable[0] == '-':
            # Storing the number after the negative value to allow comparison
            self.state = False
            self.variable = int(variable[1:])
        else:
            self.variable = int(variable)    

    def value(self):
        if not self.state:
            return -1 * self.variable
        return self.variable

    # Returns variable without sign
    def get_variable(self):
        return self.variable

    def __str__(self):
        # print ('TO STRING')
        return str(self.value())

    # Checks if the other literal has the same variable.
    def __eq__(self, that):
        # TODO can potentiall return the variable with the sign instead
        if self.variable == that.variable:
            return True
        return False

    def set_state(self, val):
        self.state = val
        
class Clause:
    def __init__(self, literals = []):
        self.literals = []
        for val in literals:
            literal = Literal(val)
            self.literals.append(literal)

    def insert_literal(self, literal):
        self.literals.append(literal)

    def get_literal(self, index):
        return self.literals[index]

    def pop(self, index = -1):
        return self.literals.pop(index)
        
    def __str__(self):
        string = ''
        for literal in self.literals:
            string += str(literal) + ' '
        return string

    def contains_literal(self, literal):
        if literal in self.literals:
            return True
        return False

    def contains_value(self, value):
        literal = Literal(value)
        return self.contains_literal(literal)

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

    def get_literal_variable(self, index):
        return self.literals[index].get_variable()

class Edge:
    def __init__(self, w, v):
        self.w = w
        self.v = v

    def __eq__(self, value):
        if self.w == value.w and self.v == value.v:
            return True
        elif self.w == value.v and self.v == value.w:
            return True
        return False

    def color_clauses(self):
        # Write a way to get the edge clauses
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
    def __str__(self):
        return 'e ' + str(self.w.get_value()) + ' ' + str(self.v.get_value())
        
class Node:
    def __init__(self, val):
        assert int(val) >= 1
        self.literal = Literal(val)
        self.color = Clause()

    def add_color(self, val):
        color_literal = Literal(str(val))
        self.color.insert_literal(color_literal)

    def get_color(self, index):
        return self.color.get_literal(index)

    def __eq__(self, that):
        if self.literal == that.literal:
            return True
        # TODO Perhaps add color checking in the future
        return False

    def __str__(self):
        return str(self.color)

    def num_colors(self):
        return len(self.color)

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

    def get_value(self):
        return self.literal.variable