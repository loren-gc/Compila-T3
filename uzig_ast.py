class Program:
    def __init__(self, statement_list):
        self.statement_list = statement_list
    def __repr__(self):
        return f'Program({self.statement_list})'

class Assignment:
    def __init__(self, location, expression):
        self.location = location
        self.expression = expression
    def __repr__(self):
        return f'Assignment({self.location}, {self.expression})'

class VariableDefinition:
    def __init__(self, name, type, expression):
        self.name = name
        self.type = type
        self.expression = expression
    def __repr__(self):
        return f'VariableDefinition({self.name!r}, {self.type}, {self.expression})'

class ConstDefinition:
    def __init__(self, name, type, expression):
        self.name = name
        self.type = type
        self.expression = expression
    def __repr__(self):
        return f'ConstDefinition({self.name!r}, {self.type}, {self.expression})'

class IfStatement:
    def __init__(self, condition, true_block, false_block):
        self.condition = condition
        self.true_block = true_block
        self.false_block = false_block
    def __repr__(self):
        return f'IfStatement({self.condition}, {self.true_block}, {self.false_block})'

class WhileStatement:
    def __init__(self, condition, block):
        self.condition = condition
        self.block = block
    def __repr__(self):
        return f'WhileStatement({self.condition}, {self.block})'

class BreakStatement:
    def __repr__(self):
        return 'BreakStatement()'

class ContinueStatement:
    def __repr__(self):
        return 'ContinueStatement()'

class ExpressionStatement:
    def __init__(self, expression):
        self.expression = expression
    def __repr__(self):
        return f'ExpressionStatement({self.expression})'

class Block:
    def __init__(self, statement_list):
        self.statement_list = statement_list
    def __repr__(self):
        return f'Block({self.statement_list})'

class BinaryOp:
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right
    def __repr__(self):
        return f'BinaryOp({self.op!r}, {self.left}, {self.right})'

class UnaryOp:
    def __init__(self, op, operand):
        self.op = op
        self.operand = operand
    def __repr__(self):
        return f'UnaryOp({self.op!r}, {self.operand})'

class Literal:
    def __init__(self, dtype, value):
        self.dtype = dtype
        self.value = value
    def __repr__(self):
        return f'Literal({self.dtype!r}, {self.value!r})'

class Location:
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return f'Location({self.name!r})'

class Builtin:
    def __init__(self, name, expression_list):
        self.name = name
        self.expression_list = expression_list
    def __repr__(self):
        return f'Builtin({self.name!r}, {self.expression_list})'

class Type:
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return f'Type({self.name!r})'

def to_source(node, indent=''):
    if isinstance(node, Program):
        return ''.join(to_source(stmt, indent) for stmt in node.statement_list)
    
    elif isinstance(node, Assignment):
        return f"{indent}{to_source(node.location)} = {to_source(node.expression)};\n"
    
    elif isinstance(node, VariableDefinition):
        res = f"{indent}var {node.name}"
        if node.type:
            res += f" : {to_source(node.type)}"
        if node.expression:
            res += f" = {to_source(node.expression)}"
        res += ";\n"
        return res
    
    elif isinstance(node, ConstDefinition):
        res = f"{indent}const {node.name}"
        if node.type:
            res += f" : {to_source(node.type)}"
        if node.expression:
            res += f" = {to_source(node.expression)}"
        res += ";\n"
        return res
    
    elif isinstance(node, IfStatement):
        res = f"{indent}if ( {to_source(node.condition)} )\n{to_source(node.true_block, indent)}"
        if node.false_block:
            if isinstance(node.false_block, IfStatement):
                res = res.rstrip() + f" else {to_source(node.false_block, indent).lstrip()}"
            else:
                res = res.rstrip() + f"\n{indent}else\n{to_source(node.false_block, indent)}"
        return res
    
    elif isinstance(node, WhileStatement):
        return f"{indent}while ( {to_source(node.condition)} )\n{to_source(node.block, indent)}"
    
    elif isinstance(node, BreakStatement):
        return f"{indent}break;\n"
    
    elif isinstance(node, ContinueStatement):
        return f"{indent}continue;\n"
    
    elif isinstance(node, ExpressionStatement):
        if node.expression is None:
            return f"{indent};\n"
        return f"{indent}{to_source(node.expression)};\n"
    
    elif isinstance(node, Block):
        if not node.statement_list:
            return f"{indent}{{\n{indent}}}\n"
        res = f"{indent}{{\n"
        for stmt in node.statement_list:
            res += to_source(stmt, indent + "    ")
        res += f"{indent}}}\n"
        return res
    
    elif isinstance(node, BinaryOp):
        return f"{to_source(node.left)} {node.op} {to_source(node.right)}"
    
    elif isinstance(node, UnaryOp):
        return f"{node.op}{to_source(node.operand)}"
    
    elif isinstance(node, Literal):
        if isinstance(node.value, bool):
            return 'true' if node.value else 'false'
        return str(node.value)
    
    elif isinstance(node, Location):
        return str(node.name)
    
    elif isinstance(node, Builtin):
        args = ", ".join(to_source(expr) for expr in node.expression_list)
        if args:
            return f"{node.name}( {args} )"
        else:
            return f"{node.name}()"
    
    elif isinstance(node, Type):
        return str(node.name)
    
    else:
        raise RuntimeError(f"Can't convert {node} to source")