class Program:
    def __init__(self, statement_list):
        self.statement_list = statement_list

class Assignment:
    def __init__(self, location, expression):
        self.location = location
        self.expression = expression

class VariableDefinition:
    def __init__(self, name, type, expression):
        self.name = name
        self.type = type
        self.expression = expression

class ConstDefinition:
    def __init__(self, name, type, expression):
        self.name = name
        self.type = type
        self.expression = expression

class IfStatement:
    def __init__(self, condition, true_block, false_block):
        self.condition = condition
        self.true_block = true_block
        self.false_block = false_block

class WhileStatement:
    def __init__(self, condition, block):
        self.condition = condition
        self.block = block

class BreakStatement:
    def __init__(self):
        pass

class ContinueStatement:
    def __init__(self):
        pass

class ExpressionStatement:
    def __init__(self, expression):
        self.expression = expression

class Block:
    def __init__(self, statement_list):
        self.statement_list = statement_list

class BinaryOp:
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

class UnaryOp:
    def __init__(self, op, operand):
        self.op = op
        self.operand = operand

class Literal:
    def __init__(self, dtype, value):
        self.dtype = dtype
        self.value = value

class Location:
    def __init__(self, name):
        self.name = name

class PrintStatement:
    def __init__(self, expressions):
        self.expressions = expressions

class Type:
    def __init__(self, name):
        self.name = name