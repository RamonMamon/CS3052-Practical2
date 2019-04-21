import copy

class Literal:
    def __init__(self, variable):
        self.state = True
        self.variable = 0

        if '--' in variable:
            raise ValueError
        elif variable[0] == '-':
            # Storing the number after the negative value to allow comparison
            self.state = False
            self.variable = int(variable[1:])
        else:
            self.variable = int(variable)    

    def value(self):
        if not self.state:
            return -1 * self.variable
        return self.variable

    def __str__(self):
        # print ('TO STRING')
        return str(self.value())

    # Checks if the other literal has the same variable.
    def __eq__(self, that):
        if self.variable == that.variable:
            return True
        return False

    def set_state(self, val):
        self.state = val
        
        
class Clause:
    # literals = []
    # num_literals = 0
    def __init__(self):
        self.literals = []

    def insert_literal(self, literal):
        # Check each character and see if it's already saved
        # if literal != '0' and literal not in self.literals:
        self.literals.append(literal)
            # self.num_literals += 1

    def get_literal(self, index):
        return self.literals[index]

    def pop(self, index = -1):
        return self.literals.pop(index)
        
    def __str__(self):
        string = ''
        for literal in self.literals:
            string += str(literal) + ' '
        return string

    def at_most_one(self, index):
        clause = Clause()
        for i in range(0, len(self.literals)):
            literal = copy.deepcopy(self.literals[i])
            if i != index:
                literal.set_state(False)
                clause.insert_literal(literal)
                
        return clause
    
    def __len__(self):
        return len(self.literals)


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
        return str(self.w.value) + ' ' + str(self.v.value)
        


class Node:
    def __init__(self, val):
        if val < 1:
            raise ValueError
        self.value = val
        self.color = Clause()

    def add_color(self, val):
        color_literal = Literal(str(val))
        self.color.insert_literal(color_literal)

    def get_color(self, index):
        return self.color.get_literal(index)

    def __eq__(self, that):
        if self.value == that.value:
            return True
        # TODO Perhaps add color checking in the future
        return False

    def __str__(self):
        return str(self.color)

    def num_colors(self):
        return len(self.color)

    def get_colors(self):
        return self.color
        
    def amo_clauses(self):
        clauses = []
        length = self.num_colors()
        for i in range(0, length):
            clause = self.color.at_most_one(i)
            clauses.append(clause)
        return clauses