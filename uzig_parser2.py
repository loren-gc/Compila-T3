# High level function that takes input tokens and turns it into a syntax tree.
# This is a natural place to use some kind of generator function.

#import sys
from sly import Parser
from uzig_lexer import zigLexer
from uzig_ast import *

# class Program:
#     def __init__(self, statement_list):
#         self.statement_list = statement_list

# class Assignment:
#     def __init__(self, location, expression):
#         self.location = location
#         self.expression = expression

# class VariableDefinition:
#     def __init__(self, name, type, expression):
#         self.name = name
#         self.type = type
#         self.expression = expression

# class ConstDefinition:
#     def __init__(self, name, type, expression):
#         self.name = name
#         self.type = type
#         self.expression = expression

# class IfStatement:
#     def __init__(self, condition, true_block, false_block):
#         self.condition = condition
#         self.true_block = true_block
#         self.false_block = false_block

# class WhileStatement:
#     def __init__(self, condition, block):
#         self.condition = condition
#         self.block = block

# class BreakStatement:
#     def __init__(self):
#         pass

# class ContinueStatement:
#     def __init__(self):
#         pass

# class ExpressionStatement:
#     def __init__(self, expression):
#         self.expression = expression

# class Block:
#     def __init__(self, statement_list):
#         self.statement_list = statement_list

# class BinaryOp:
#     def __init__(self, op, left, right):
#         self.op = op
#         self.left = left
#         self.right = right

# class UnaryOp:
#     def __init__(self, op, operand):
#         self.op = op
#         self.operand = operand

# class Literal:
#     def __init__(self, dtype, value):
#         self.dtype = dtype
#         self.value = value

# class Location:
#     def __init__(self, name):
#         self.name = name

# class PrintStatement:
#     def __init__(self, expressions):
#         self.expressions = expressions

# class Type:
#     def __init__(self, name):
#         self.name = name

class zigParser(Parser):

    tokens = zigLexer.tokens
    precedence = ( 
        ('nonassoc', 'LOWER_THAN_ELSE'), ('nonassoc', 'KEYWORD_else'), ('left', 'KEYWORD_or'), ('left', 'KEYWORD_and'), ('left', 'EQUALEQUAL', 'EXCLAMATIONMARKEQUAL'), ('left', 'LARROW', 'LARROWEQUAL', 'RARROW', 'RARROWEQUAL'), ('left', 'PLUS', 'MINUS'), ('left', 'ASTERISK', 'SLASH', 'PERCENT'), ('right', 'UMINUS', 'UPLUS', 'EXCLAMATIONMARK'),
    )

    @_('statement_list')
    def program(self, p):
        return Program(p.statement_list)

    @_('statement_list statement')
    def statement_list(self, p):
        return p.statement_list + [p.statement]

    @_('statement')
    def statement_list(self, p):
        return [p.statement]

    @_('assignment_statement',
       'variable_definition',
       'const_definition',
       'if_statement',
       'while_statement',
       'break_statement',
       'continue_statement',
       'expression_statement')
    def statement(self, p):
        return p[0]

    @_('location EQUAL expression SEMI')
    def assignment_statement(self, p):
        return Assignment(p.location, p.expression)

    @_('KEYWORD_var IDENTIFIER COLON type EQUAL expression SEMI')
    def variable_definition(self, p):
        return VariableDefinition(p.IDENTIFIER, p.type, p.expression)

    @_('KEYWORD_var IDENTIFIER COLON type SEMI')
    def variable_definition(self, p):
        return VariableDefinition(p.IDENTIFIER, p.type, None)

    @_('KEYWORD_var IDENTIFIER EQUAL expression SEMI')
    def variable_definition(self, p):
        return VariableDefinition(p.IDENTIFIER, None, p.expression)

    @_('KEYWORD_const IDENTIFIER COLON type EQUAL expression SEMI')
    def const_definition(self, p):
        return ConstDefinition(p.IDENTIFIER, p.type, p.expression)

    @_('KEYWORD_const IDENTIFIER EQUAL expression SEMI')
    def const_definition(self, p):
        return ConstDefinition(p.IDENTIFIER, None, p.expression)

    @_('KEYWORD_if LPAREN expression RPAREN block %prec LOWER_THAN_ELSE')
    def if_statement(self, p):
        return IfStatement(p.expression, p.block, None)

    @_('KEYWORD_if LPAREN expression RPAREN block KEYWORD_else block')
    def if_statement(self, p):
        return IfStatement(p.expression, p.block0, p.block1)

    @_('KEYWORD_if LPAREN expression RPAREN block KEYWORD_else if_statement')
    def if_statement(self, p):
        return IfStatement(p.expression, p.block, p.if_statement)

    @_('KEYWORD_while LPAREN expression RPAREN block')
    def while_statement(self, p):
        return WhileStatement(p.expression, p.block)

    @_('KEYWORD_break SEMI')
    def break_statement(self, p):
        return BreakStatement()

    @_('KEYWORD_continue SEMI')
    def continue_statement(self, p):
        return ContinueStatement()

    @_('expression SEMI')
    def expression_statement(self, p):
        return ExpressionStatement(p.expression)

    @_('SEMI')
    def expression_statement(self, p):
        return ExpressionStatement(None)

    @_('LBRACE statement_list RBRACE')
    def block(self, p):
        return Block(p.statement_list)

    @_('LBRACE RBRACE')
    def block(self, p):
        return Block([])

    @_('expression PLUS expression',
       'expression MINUS expression',
       'expression ASTERISK expression',
       'expression SLASH expression',
       'expression PERCENT expression',
       'expression LARROWEQUAL expression',
       'expression LARROW expression',
       'expression RARROWEQUAL expression',
       'expression RARROW expression',
       'expression EQUALEQUAL expression',
       'expression EXCLAMATIONMARKEQUAL expression',
       'expression KEYWORD_and expression',
       'expression KEYWORD_or expression')
    def expression(self, p):
        return BinaryOp(p[1], p.expression0, p.expression1)

    @_('PLUS expression %prec UPLUS',
       'MINUS expression %prec UMINUS',
       'EXCLAMATIONMARK expression')
    def expression(self, p):
        return UnaryOp(p[0], p.expression)

    @_('literal')
    def expression(self, p):
        return p.literal

    @_('location')
    def expression(self, p):
        return p.location

    @_('PRINT LPAREN expression_list RPAREN')
    def expression(self, p):
        return PrintStatement(p.expression_list)

    @_('PRINT LPAREN RPAREN')
    def expression(self, p):
        return PrintStatement([])

    @_('LPAREN expression RPAREN')
    def expression(self, p):
        return p.expression

    @_('FLOAT')
    def literal(self, p):
        return Literal('f64', p.FLOAT)

    @_('INTEGER')
    def literal(self, p):
        return Literal('i32', p.INTEGER)

    @_('KEYWORD_true')
    def literal(self, p):
        return Literal('bool', True)

    @_('KEYWORD_false')
    def literal(self, p):
        return Literal('bool', False)

    @_('STRINGLITERAL')
    def literal(self, p):
        return Literal('[]const u8', p.STRINGLITERAL)

    @_('CHAR_LITERAL')
    def literal(self, p):
        return Literal('u8', p.CHAR_LITERAL)

    @_('expression')
    def expression_list(self, p):
        return [p.expression]

    @_('expression_list COMMA expression')
    def expression_list(self, p):
        return p.expression_list + [p.expression]

    @_('IDENTIFIER')
    def location(self, p):
        return Location(p.IDENTIFIER)

    @_('IDENTIFIER')
    def type(self, p):
        return Type(p.IDENTIFIER)

    def error(self, token):
        if token:
            print(f"Syntax error at line {token.lineno}, token={token.type}")
        else:
            print("Parse error in input. EOF")


def parse_tokens(token_stream):
    return zigParser().parse(token_stream)