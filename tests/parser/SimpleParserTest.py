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
    
    def testConfigBlock(self):
        """Tests parsing of a service with a configuration block.
        """
        service = self._parseService("config.txt")
        root = service.tree
        # Configuration block
        config = root.getChild(1)
        self.assertEqual(config.getType(), parser.servicegenLexer.CONFIG)
    
    def testConfigUnitialized(self):
        """
        Test parsing of a variable in the config block which is
        not initialized.
        """
        service = self._parseService("config.txt")
        root = service.tree
        config = root.getChild(1)
        var = config.getChild(0)
        self.assertEqual(var.getType(), parser.servicegenLexer.VARIABLE)
        self.assertEqual(var.getChild(0).getType(), parser.servicegenLexer.VARTYPE)
        self.assertEqual(var.getChild(0).getChild(0).getText(), 'database')
        self.assertEqual(var.getChild(1).getType(), parser.servicegenLexer.IDENTIFIER)
        self.assertEqual(var.getChild(1).getText(), 'db')
    
    def testConfigUnitializedString(self):
        """
        Testing parsing of a string variable which is not initialized.
        """
        service = self._parseService("config.txt")
        root = service.tree
        config = root.getChild(1)
        var = config.getChild(1)
        self.assertEqual(var.getType(), parser.servicegenLexer.VARIABLE)
        self.assertEqual(var.getChild(0).getType(), parser.servicegenLexer.VARTYPE)
        self.assertEqual(var.getChild(0).getChild(0).getText(), 'string')
        self.assertEqual(var.getChild(1).getType(), parser.servicegenLexer.IDENTIFIER)
        self.assertEqual(var.getChild(1).getText(), 'password')
    
    def testConfigInitializedString(self):
        """
        Testing parsing of a variable with an underline in the identifier and
        which is initialized with a string.
        """
        service = self._parseService("config.txt")
        root = service.tree
        config = root.getChild(1)
        var = config.getChild(2)
        self.assertEqual(var.getType(), parser.servicegenLexer.VARIABLE)
        self.assertEqual(var.getChild(0).getType(), parser.servicegenLexer.VARTYPE)
        self.assertEqual(var.getChild(0).getChild(0).getText(), 'string')
        self.assertEqual(var.getChild(1).getType(), parser.servicegenLexer.IDENTIFIER)
        self.assertEqual(var.getChild(1).getText(), 'user_name')
        self.assertEqual(var.getChild(2).getType(), parser.servicegenLexer.LITERAL_STRING)
        self.assertEqual(var.getChild(2).getChild(0).getText(), '"myuser"')
    
    def testConfigInitializedInt(self):
        """
        Testing parsing of a variable which is initialized with an int.
        """
        service = self._parseService("config.txt")
        root = service.tree
        config = root.getChild(1)
        var = config.getChild(3)
        self.assertEqual(var.getType(), parser.servicegenLexer.VARIABLE)
        self.assertEqual(var.getChild(0).getType(), parser.servicegenLexer.VARTYPE)
        self.assertEqual(var.getChild(0).getChild(0).getText(), 'int')
        self.assertEqual(var.getChild(1).getType(), parser.servicegenLexer.IDENTIFIER)
        self.assertEqual(var.getChild(1).getText(), 'stations')
        self.assertEqual(var.getChild(2).getType(), parser.servicegenLexer.LITERAL_INT)
        self.assertEqual(var.getChild(2).getChild(0).getText(), '10')
    
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
        self.assertEqual(var.getChild(1).getText(), 'user_name')
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
        validate = root.getChild(1).getChild(2)
        self.assertEqual(validate.getType(), parser.servicegenLexer.FUNCTION_CALL)
        self.assertEqual(validate.getChild(0).getType(), parser.servicegenLexer.VARREF)
        self.assertEqual(validate.getChild(0).getChild(0).getText(), 'zip')
        self.assertEqual(validate.getChild(1).getType(), parser.servicegenLexer.LITERAL_REGEXP)
        self.assertEqual(validate.getChild(1).getChild(0).getText(), '/[0-9]{4}/')
    
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
    
    def testVariableCache(self):
        """
        Tests caching keyword of a variable.
        """
        service = self._parseService("variable.txt")
        root = service.tree
        var = root.getChild(1).getChild(4)
        self.assertEqual(var.getType(), parser.servicegenLexer.VARIABLE)
        self.assertEqual(var.getChild(0).getType(), parser.servicegenLexer.VARTYPE)
        self.assertEqual(var.getChild(0).getChild(0).getText(), 'int')
        self.assertEqual(var.getChild(1).getType(), parser.servicegenLexer.CACHE)
        self.assertEqual(var.getChild(1).getChild(0).getType(), parser.servicegenLexer.DURATION_DAYS)
        self.assertEqual(var.getChild(1).getChild(0).getChild(0).getText(), '1')
        self.assertEqual(var.getChild(2).getType(), parser.servicegenLexer.IDENTIFIER)
        self.assertEqual(var.getChild(2).getText(), 'cachedForOneDay')
        self.assertEqual(var.getChild(3).getType(), parser.servicegenLexer.LITERAL_INT)
        self.assertEqual(var.getChild(3).getChild(0).getText(), '3')
    
    def testDurations(self):
        """Various durations."""
        service = self._parseService("variable.txt")
        root = service.tree
        request = root.getChild(1)
        self.assertEqual(request.getChild(5).getChild(1).getChild(0).getType(), parser.servicegenLexer.DURATION_MINUTES)
        self.assertEqual(request.getChild(6).getChild(1).getChild(0).getType(), parser.servicegenLexer.DURATION_HOURS)
        self.assertEqual(request.getChild(7).getChild(1).getChild(0).getType(), parser.servicegenLexer.DURATION_SECONDS)
        self.assertEqual(request.getChild(8).getChild(1).getChild(0).getType(), parser.servicegenLexer.DURATION_DAYS)
        self.assertEqual(request.getChild(9).getChild(1).getChild(0).getType(), parser.servicegenLexer.DURATION_MINUTES)
        self.assertEqual(request.getChild(10).getChild(1).getChild(0).getType(), parser.servicegenLexer.DURATION_HOURS)
        self.assertEqual(request.getChild(11).getChild(1).getChild(0).getType(), parser.servicegenLexer.DURATION_SECONDS)
    
    def testSql(self):
        """
        Tests assignment of a variable which consists of an SQL query.
        """
        service = self._parseService("sql.txt")
        root = service.tree
        request = root.getChild(1)
        self.assertEqual(request.getChild(2).getType(), parser.servicegenLexer.VARIABLE)
        self.assertEqual(request.getChild(2).getChild(0).getType(), parser.servicegenLexer.VARTYPE)
        self.assertEqual(request.getChild(2).getChild(0).getChild(0).getText(), 'records')
        self.assertEqual(request.getChild(2).getChild(1).getType(), parser.servicegenLexer.IDENTIFIER)
        self.assertEqual(request.getChild(2).getChild(1).getText(), 'weather')
        self.assertEqual(request.getChild(2).getChild(2).getType(), parser.servicegenLexer.LITERAL_SQL)
        self.assertEqual(request.getChild(2).getChild(2).getChild(0).getText(), 'SELECT * FROM weather WHERE zip={zip} ORDER BY date ASC')
    
    def testOutput(self):
        """
        Tests parsing of output blocks. Currently everything inside the
        output block is just returned as statements.
        """
        service = self._parseService("output.txt")
        root = service.tree
        output = root.getChild(1).getChild(2)
        self.assertEqual(output.getType(), parser.servicegenLexer.STATEMENT_OUTPUT)
        self.assertEqual(output.getChild(0).getText(), 'xml')
    
    def testOutputVariableReference(self):
        """
        Tests parsing of variable references inside the output block.
        """
        service = self._parseService("output.txt")
        root = service.tree
        var = root.getChild(1).getChild(2).getChild(1)
        self.assertEqual(var.getType(), parser.servicegenLexer.VARREF)
        self.assertEqual(var.getChild(0).getText(), 'zip')
    
    def testOutputString(self):
        """
        Tests parsing of string literals inside the output block.
        """
        service = self._parseService("output.txt")
        root = service.tree
        literal = root.getChild(1).getChild(2).getChild(2)
        self.assertEqual(literal.getType(), parser.servicegenLexer.LITERAL_STRING)
        self.assertEqual(literal.getChild(0).getText(), '"<ml>this is my string</ml>"')
    
    def testFunctionCall(self):
        """
        Call functions for variable assignments.
        """
        service = self._parseService("members.txt")
        root = service.tree
        var = root.getChild(3).getChild(4)
        self.assertEqual(var.getType(), parser.servicegenLexer.VARIABLE)
        self.assertEqual(var.getChild(0).getType(), parser.servicegenLexer.VARTYPE)
        self.assertEqual(var.getChild(0).getChild(0).getText(), 'hash')
        self.assertEqual(var.getChild(1).getType(), parser.servicegenLexer.IDENTIFIER)
        self.assertEqual(var.getChild(1).getText(), 'stations')
        self.assertEqual(var.getChild(2).getType(), parser.servicegenLexer.FUNCTION_CALL)
        self.assertEqual(var.getChild(2).getChild(0).getType(), parser.servicegenLexer.VARREF)
        self.assertEqual(var.getChild(2).getChild(0).getChild(0).getText(), 'locations')
        self.assertEqual(var.getChild(2).getChild(1).getType(), parser.servicegenLexer.LITERAL_STRING)
        self.assertEqual(var.getChild(2).getChild(1).getChild(0).getText(), '"stations"')
        self.assertEqual(var.getChild(2).getChild(2).getType(), parser.servicegenLexer.VARREF)
        self.assertEqual(var.getChild(2).getChild(2).getChild(0).getText(), 'x')
        self.assertEqual(var.getChild(2).getChild(3).getType(), parser.servicegenLexer.VARREF)
        self.assertEqual(var.getChild(2).getChild(3).getChild(0).getText(), 'y')
    
    def testExternal(self):
        """
        Define externals members inside the service definition.
        """
        service = self._parseService("members.txt")
        root = service.tree
        external = root.getChild(2)
        self.assertEqual(external.getType(), parser.servicegenLexer.EXTERNAL)
        self.assertEqual(external.getChild(0).getText(), "php")
        self.assertEqual(external.getChild(1).getText(), '"filename.php"')
    
    def _parseService(self, service):
        """Parses the service from the given file."""
        s = Service()
        return s.parse("tests/services/" + service)

if __name__ == '__main__':
    unittest.main()
