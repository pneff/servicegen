import unittest
from parser.Service import Service
from parser.servicegenLexer import servicegenLexer
from tools.Service import DumpTree
import parser.servicegenLexer

class SimpleParserTest(unittest.TestCase):
    def testBasic(self):
        """
        Tests parsing of a very basic service. Just contains the service
        name, nothing else.
        """
        service = self._parseService("basic.txt")
        root = service.tree
        self.assertEqual(root.getType(), parser.servicegenLexer.SERVICE)
        self.assertEqual(root.getChild(0).getType(), parser.servicegenLexer.IDENTIFIER)
        self.assertEqual(root.getChild(0).getText(), 'meteo')
    
    def testConfig(self):
        """Tests parsing of a service with a configuration block.
        """
        service = self._parseService("config.txt")
        root = service.tree
        # Service
        self.assertEqual(root.getChild(0).getType(), parser.servicegenLexer.SERVICE)
        self.assertEqual(root.getChild(0).getChild(0).getText(), 'meteo')
        # Configuration block
        config = root.getChild(1)
        self.assertEqual(config.getType(), parser.servicegenLexer.CONFIG)
        # Variable 1: database: db
        var = config.getChild(0)
        self.assertEqual(var.getType(), parser.servicegenLexer.VARIABLE)
        self.assertEqual(var.getChild(0).getType(), parser.servicegenLexer.VARTYPE)
        self.assertEqual(var.getChild(0).getChild(0).getText(), 'database')
        self.assertEqual(var.getChild(1).getType(), parser.servicegenLexer.IDENTIFIER)
        self.assertEqual(var.getChild(1).getText(), 'db')
        # Variable 2: string: password
        var = config.getChild(1)
        self.assertEqual(var.getType(), parser.servicegenLexer.VARIABLE)
        self.assertEqual(var.getChild(0).getType(), parser.servicegenLexer.VARTYPE)
        self.assertEqual(var.getChild(0).getChild(0).getText(), 'string')
        self.assertEqual(var.getChild(1).getType(), parser.servicegenLexer.IDENTIFIER)
        self.assertEqual(var.getChild(1).getText(), 'password')
        # Variable 2: string: user
        var = config.getChild(2)
        self.assertEqual(var.getType(), parser.servicegenLexer.VARIABLE)
        self.assertEqual(var.getChild(0).getType(), parser.servicegenLexer.VARTYPE)
        self.assertEqual(var.getChild(0).getChild(0).getText(), 'string')
        self.assertEqual(var.getChild(1).getType(), parser.servicegenLexer.IDENTIFIER)
        self.assertEqual(var.getChild(1).getText(), 'user')
        self.assertEqual(var.getChild(2).getType(), parser.servicegenLexer.LITERAL_STRING)
        self.assertEqual(var.getChild(2).getChild(0).getText(), '"myuser"')
    
    def testRequest(self):
        """Tests parsing of a service with one defined request.
        """
        service = self._parseService("request.txt")
        root = service.tree
        request = root.getChild(1)
        self.assertEqual(request.getType(), parser.servicegenLexer.REQUEST)
        self.assertEqual(request.getChild(0).getType(), parser.servicegenLexer.HTTP_METHOD)
        self.assertEqual(request.getChild(0).getText(), 'GET')
        self.assertEqual(request.getChild(1).getType(), parser.servicegenLexer.REQUEST_PATH)
        self.assertEqual(request.getChild(1).getChild(0).getText(), '"/testing/this/path"')
    
    def testVariable(self):
        """
        Tests parsing of a service with one defined request which takes
        a parameter.
        """
        service = self._parseService("variable.txt")
        root = service.tree
        request = root.getChild(1)
        self.assertEqual(request.getType(), parser.servicegenLexer.REQUEST)
        self.assertEqual(request.getChild(0).getType(), parser.servicegenLexer.HTTP_METHOD)
        self.assertEqual(request.getChild(0).getText(), 'GET')
        self.assertEqual(request.getChild(1).getType(), parser.servicegenLexer.REQUEST_PATH)
        self.assertEqual(request.getChild(1).getChild(0).getText(), '"/{zip}"')
        
    def testVariableValidation(self):
        """
        Tests parsing of a service with one defined regexp validation.
        """
        service = self._parseService("variable.txt")
        root = service.tree
        request = root.getChild(1)
        self.assertEqual(request.getChild(2).getType(), parser.servicegenLexer.STATEMENT_VALIDATE)
        self.assertEqual(request.getChild(2).getChild(0).getType(), parser.servicegenLexer.IDENTIFIER)
        self.assertEqual(request.getChild(2).getChild(0).getText(), 'zip')
        self.assertEqual(request.getChild(2).getChild(1).getType(), parser.servicegenLexer.LITERAL_REGEXP)
        self.assertEqual(request.getChild(2).getChild(1).getChild(0).getText(), '/[0-9]{4}/')
        
    def testVariableAssignment(self):
        """
        Tests assignment of a variable inside a request body.
        """
        service = self._parseService("variable.txt")
        root = service.tree
        request = root.getChild(1)
        self.assertEqual(request.getChild(3).getType(), parser.servicegenLexer.VARIABLE)
        self.assertEqual(request.getChild(3).getChild(0).getType(), parser.servicegenLexer.VARTYPE)
        self.assertEqual(request.getChild(3).getChild(0).getChild(0).getText(), 'string')
        self.assertEqual(request.getChild(3).getChild(1).getType(), parser.servicegenLexer.IDENTIFIER)
        self.assertEqual(request.getChild(3).getChild(1).getText(), 'var')
        self.assertEqual(request.getChild(3).getChild(2).getType(), parser.servicegenLexer.LITERAL_STRING)
        self.assertEqual(request.getChild(3).getChild(2).getChild(0).getText(), '"2"')
    
    def _parseService(self, service):
        """Parses the service from the given file."""
        s = Service()
        return s.parse("tests/services/" + service)

if __name__ == '__main__':
    unittest.main()
