import sys
import antlr3
from servicegenLexer import servicegenLexer
from servicegenParser import servicegenParser

class Service:
    """Parses a service description and returns the parse tree."""
    def parse(self, file):
        f = open(file, "r")
        char_stream = antlr3.ANTLRStringStream(f.read())
        f.close()
        
        lexer = servicegenLexer(char_stream)
        tokens = antlr3.CommonTokenStream(lexer)
        parser = servicegenParser(tokens)
        return parser.declaration()
