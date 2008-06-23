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
        self.assertEqual(var.getChild(2).getChild(0).getText(), 'myuser')
    
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
    
    def testConfigInitializedStringEscaped(self):
        """
        Testing parsing of a string with embedded quotes
        """
        service = self._parseService("config.txt")
        root = service.tree
        config = root.getChild(1)
        var = config.getChild(4)
        self.assertEqual(var.getType(), parser.servicegenLexer.VARIABLE)
        self.assertEqual(var.getChild(0).getType(), parser.servicegenLexer.VARTYPE)
        self.assertEqual(var.getChild(0).getChild(0).getText(), 'string')
        self.assertEqual(var.getChild(1).getType(), parser.servicegenLexer.IDENTIFIER)
        self.assertEqual(var.getChild(1).getText(), 'escaped')
        self.assertEqual(var.getChild(2).getType(), parser.servicegenLexer.LITERAL_STRING)
        self.assertEqual(var.getChild(2).getChild(0).getText(), 'my"test var')
    
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
        self.assertEqual(var.getChild(2).getChild(0).getText(), 'myuser')
    
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
        self.assertEqual(request.getChild(1).getChild(0).getText(), '/testing/this/path')
    
    def testRequestName(self):
        """
        Tests parsing of a request with a name.
        """
        service = self._parseService("request.txt")
        root = service.tree
        request = root.getChild(2)
        self.assertEqual(request.getType(), parser.servicegenLexer.REQUEST)
        self.assertEqual(request.getChild(0).getType(), parser.servicegenLexer.HTTP_METHOD)
        self.assertEqual(request.getChild(0).getText(), 'POST')
        self.assertEqual(request.getChild(1).getType(), parser.servicegenLexer.REQUEST_PATH)
        self.assertEqual(request.getChild(1).getChild(0).getText(), '/anotherpath')
        self.assertEqual(request.getChild(5).getType(), parser.servicegenLexer.REQUEST_NAME)
        self.assertEqual(request.getChild(5).getChild(0).getText(), 'SaveSomething')
    
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
        self.assertEqual(request.getChild(1).getChild(0).getText(), '/{zip}')
        
    def testVariableValidation(self):
        """
        Tests parsing of a service with one defined regexp validation.
        """
        service = self._parseService("variable.txt")
        root = service.tree
        validate = root.getChild(1).getChild(3).getChild(0)
        self.assertEqual(validate.getType(), parser.servicegenLexer.FUNCTION_CALL)
        self.assertEqual(validate.getChild(0).getType(), parser.servicegenLexer.FUNCTION_NAME_BUILTIN)
        self.assertEqual(validate.getChild(0).getChild(0).getText(), 'validate')
        self.assertEqual(validate.getChild(1).getType(), parser.servicegenLexer.VARREF)
        self.assertEqual(validate.getChild(1).getChild(0).getText(), 'zip')
        self.assertEqual(validate.getChild(2).getType(), parser.servicegenLexer.LITERAL_REGEXP)
        self.assertEqual(validate.getChild(2).getChild(0).getText(), '/[0-9]{4}/')
    
    def testVariableAssignment(self):
        """
        Tests assignment of a variable inside a request body.
        """
        service = self._parseService("variable.txt")
        root = service.tree
        variable = root.getChild(1).getChild(3).getChild(1)
        self.assertEqual(variable.getType(), parser.servicegenLexer.VARIABLE)
        self.assertEqual(variable.getChild(0).getType(), parser.servicegenLexer.VARTYPE)
        self.assertEqual(variable.getChild(0).getChild(0).getText(), 'string')
        self.assertEqual(variable.getChild(1).getType(), parser.servicegenLexer.IDENTIFIER)
        self.assertEqual(variable.getChild(1).getText(), 'var')
        self.assertEqual(variable.getChild(2).getType(), parser.servicegenLexer.LITERAL_STRING)
        self.assertEqual(variable.getChild(2).getChild(0).getText(), '2')
    
    def testVariableCache(self):
        """
        Tests caching keyword of a variable.
        """
        service = self._parseService("variable.txt")
        root = service.tree
        var = root.getChild(1).getChild(3).getChild(2)
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
    
    def testXmlLiteral(self):
        """
        Tests XML literals.
        """
        service = self._parseService("variable.txt")
        root = service.tree
        var = root.getChild(1).getChild(3).getChild(10)
        self.assertEqual(var.getChild(2).getType(), parser.servicegenLexer.LITERAL_XML)
        self.assertEqual(var.getChild(2).getChild(0).getText(), '<')
        self.assertEqual(var.getChild(2).getChild(1).getText(), 'testing')
        self.assertEqual(var.getChild(2).getChild(2).getText(), '>')
    
    def testXmlLiteralClosing(self):
        """
        Tests closing tag XML literal.
        """
        service = self._parseService("variable.txt")
        root = service.tree
        var = root.getChild(1).getChild(3).getChild(11)
        self.assertEqual(var.getChild(2).getType(), parser.servicegenLexer.LITERAL_XML)
        self.assertEqual(var.getChild(2).getChild(0).getText(), '</')
        self.assertEqual(var.getChild(2).getChild(1).getText(), 'testing')
        self.assertEqual(var.getChild(2).getChild(2).getText(), '>')
    
    def testDurations(self):
        """Various durations."""
        service = self._parseService("variable.txt")
        root = service.tree
        request = root.getChild(1).getChild(3)
        self.assertEqual(request.getChild(3).getChild(1).getChild(0).getType(), parser.servicegenLexer.DURATION_MINUTES)
        self.assertEqual(request.getChild(4).getChild(1).getChild(0).getType(), parser.servicegenLexer.DURATION_HOURS)
        self.assertEqual(request.getChild(5).getChild(1).getChild(0).getType(), parser.servicegenLexer.DURATION_SECONDS)
        self.assertEqual(request.getChild(6).getChild(1).getChild(0).getType(), parser.servicegenLexer.DURATION_DAYS)
        self.assertEqual(request.getChild(7).getChild(1).getChild(0).getType(), parser.servicegenLexer.DURATION_MINUTES)
        self.assertEqual(request.getChild(8).getChild(1).getChild(0).getType(), parser.servicegenLexer.DURATION_HOURS)
        self.assertEqual(request.getChild(9).getChild(1).getChild(0).getType(), parser.servicegenLexer.DURATION_SECONDS)
    
    def testOutput(self):
        """
        Tests parsing of output blocks. Currently everything inside the
        output block is just returned as statements.
        """
        service = self._parseService("output.txt")
        root = service.tree
        output = service.tree.getChild(2).getChild(4).getChild(0)
        self.assertEqual(output.getType(), parser.servicegenLexer.STATEMENT_OUTPUT)
        self.assertEqual(output.getChild(0).getText(), 'xml')
    
    def testOutputCondensed(self):
        """
        Tests parsing of output blocks when one output block defines two
        formats.
        """
        service = self._parseService("output.txt")
        root = service.tree
        # Outputs get duplicated. 1st XML
        output = service.tree.getChild(3).getChild(4).getChild(0)
        self.assertEqual(output.getType(), parser.servicegenLexer.STATEMENT_OUTPUT)
        self.assertEqual(output.getChild(0).getText(), 'xml')
        # 2nd CSV
        output = service.tree.getChild(3).getChild(4).getChild(1)
        self.assertEqual(output.getType(), parser.servicegenLexer.STATEMENT_OUTPUT)
        self.assertEqual(output.getChild(0).getText(), 'csv')
    
    def testOutputVariableReference(self):
        """
        Tests parsing of variable references inside the output block.
        """
        service = self._parseService("output.txt")
        root = service.tree
        var = root.getChild(1).getChild(4).getChild(0).getChild(1)
        self.assertEqual(var.getType(), parser.servicegenLexer.VARREF)
        self.assertEqual(var.getChild(0).getText(), 'zip')
    
    def testOutputString(self):
        """
        Tests parsing of string literals inside the output block.
        """
        service = self._parseService("output.txt")
        root = service.tree
        literal = root.getChild(1).getChild(4).getChild(0).getChild(2)
        self.assertEqual(literal.getType(), parser.servicegenLexer.LITERAL_STRING)
        self.assertEqual(literal.getChild(0).getText(), '<ml>this is my string</ml>')
    
    def testOutputCache(self):
        """
        Tests cache of an output block.
        """
        service = self._parseService("output.txt")
        output = service.tree.getChild(2).getChild(4).getChild(0)
        self.assertEqual(output.getType(), parser.servicegenLexer.STATEMENT_OUTPUT)
        self.assertEqual(output.getChild(1).getType(), parser.servicegenLexer.CACHE)
        self.assertEqual(output.getChild(1).getChild(0).getType(), parser.servicegenLexer.DURATION_MONTHS)
        self.assertEqual(output.getChild(1).getChild(0).getChild(0).getText(), '8')
    
    def testFunctionCall(self):
        """
        Call functions for variable assignments.
        """
        service = self._parseService("members.txt")
        root = service.tree
        var = root.getChild(3).getChild(3).getChild(2)
        self.assertEqual(var.getType(), parser.servicegenLexer.VARIABLE)
        self.assertEqual(var.getChild(0).getType(), parser.servicegenLexer.VARTYPE)
        self.assertEqual(var.getChild(0).getChild(0).getText(), 'hash')
        self.assertEqual(var.getChild(1).getType(), parser.servicegenLexer.IDENTIFIER)
        self.assertEqual(var.getChild(1).getText(), 'stations')
        self.assertEqual(var.getChild(2).getType(), parser.servicegenLexer.FUNCTION_CALL)
        self.assertEqual(var.getChild(2).getChild(0).getType(), parser.servicegenLexer.FUNCTION_NAME_USER)
        self.assertEqual(var.getChild(2).getChild(0).getChild(0).getText(), 'getStations')
        self.assertEqual(var.getChild(2).getChild(1).getType(), parser.servicegenLexer.VARREF)
        self.assertEqual(var.getChild(2).getChild(1).getChild(0).getText(), 'locations')
        self.assertEqual(var.getChild(2).getChild(2).getType(), parser.servicegenLexer.LITERAL_STRING)
        self.assertEqual(var.getChild(2).getChild(2).getChild(0).getText(), 'stations')
        self.assertEqual(var.getChild(2).getChild(3).getType(), parser.servicegenLexer.VARREF)
        self.assertEqual(var.getChild(2).getChild(3).getChild(0).getText(), 'x')
        self.assertEqual(var.getChild(2).getChild(4).getType(), parser.servicegenLexer.VARREF)
        self.assertEqual(var.getChild(2).getChild(4).getChild(0).getText(), 'y')
    
    def testFunctionCallWithDot(self):
        """
        Call a function with a dot.
        """
        service = self._parseService("members.txt")
        root = service.tree
        var = root.getChild(3).getChild(3).getChild(3)
        self.assertEqual(var.getChild(2).getType(), parser.servicegenLexer.FUNCTION_CALL)
        self.assertEqual(var.getChild(2).getChild(0).getType(), parser.servicegenLexer.FUNCTION_NAME_USER)
        self.assertEqual(var.getChild(2).getChild(0).getChild(0).getText(), 'data.getStations')
    
    def testExternal(self):
        """
        Define externals members inside the service definition.
        """
        service = self._parseService("members.txt")
        root = service.tree
        external = root.getChild(2)
        self.assertEqual(external.getType(), parser.servicegenLexer.EXTERNAL)
        self.assertEqual(external.getChild(0).getText(), "php")
        self.assertEqual(external.getChild(1).getText(), 'filename.php')
    
    def testDocumentationServiceDoc(self):
        """Tests the description documentation tags of the service."""
        service = self._parseService("docs.txt").tree.getChild(0)
        self.assertEqual(service.getChild(1).getType(), parser.servicegenLexer.DOC)
        self.assertEqual(service.getChild(1).getChild(0).getText(), "doc")
        self.assertEqual(service.getChild(1).getChild(1).getText(), 'Provides weather forecast information for Switzerland.')
    
    def testDocumentationServiceAuthor(self):
        """Tests the author documentation tag of the service."""
        service = self._parseService("docs.txt").tree.getChild(0)
        self.assertEqual(service.getChild(2).getType(), parser.servicegenLexer.DOC)
        self.assertEqual(service.getChild(2).getChild(0).getText(), "author")
        self.assertEqual(service.getChild(2).getChild(1).getText(), 'Patrice Neff')
    
    def testDocumentationServiceVersion(self):
        """Tests the version documentation tag of the service."""
        service = self._parseService("docs.txt").tree.getChild(0)
        self.assertEqual(service.getChild(3).getType(), parser.servicegenLexer.DOC)
        self.assertEqual(service.getChild(3).getChild(0).getText(), "version")
        self.assertEqual(service.getChild(3).getChild(1).getText(), '1.0')
    
    def testDocumentationConfigVar(self):
        """Tests the documentation of a config variable."""
        cfgvar = self._parseService("docs.txt").tree.getChild(1).getChild(0)
        self.assertEqual(cfgvar.getChild(2).getType(), parser.servicegenLexer.DOC_FOR)
        self.assertEqual(cfgvar.getChild(2).getChild(0).getText(), "db")
        self.assertEqual(cfgvar.getChild(2).getChild(1).getText(), 'Database containing the weather information. Must have a table \'weather\' with one entry per day.')
    
    def testDocumentationRequest(self):
        """Tests the documentation of a request block."""
        request = self._parseService("docs.txt").tree.getChild(2)
        self.assertEqual(request.getChild(5).getType(), parser.servicegenLexer.DOC)
        self.assertEqual(request.getChild(5).getChild(0).getText(), "doc")
        self.assertEqual(request.getChild(5).getChild(1).getText(), 'Returns all available forecasts for a ZIP code in Switzerland.')
    
    def testDocumentationRequestParam(self):
        """Tests the documentation of a request param."""
        request = self._parseService("docs.txt").tree.getChild(2)
        self.assertEqual(request.getChild(6).getType(), parser.servicegenLexer.DOC_FOR)
        self.assertEqual(request.getChild(6).getChild(0).getText(), "zip")
        self.assertEqual(request.getChild(6).getChild(1).getText(), 'ZIP code for which to get weather forecast')
    
    def testDocumentationOutput(self):
        """Tests the documentation of an output block."""
        output = self._parseService("docs.txt").tree.getChild(2).getChild(4).getChild(0)
        self.assertEqual(output.getChild(1).getType(), parser.servicegenLexer.DOC)
        self.assertEqual(output.getChild(1).getChild(0).getText(), "doc")
        self.assertEqual(output.getChild(1).getChild(1).getText(), 'Returns the weather forecast in XML format.')
    
    def testPostData(self):
        """Tests the declaration of POST parameters."""
        request = self._parseService("post.txt").tree.getChild(1)
        postparams = request.getChild(2)
        self.assertEqual(postparams.getChildCount(), 2)
        self.assertEqual(postparams.getChild(0).getText(), 'key')
        self.assertEqual(postparams.getChild(1).getText(), 'value')
    
    def testPostDataWildcard(self):
        """Tests the declaration of POST parameters with a wildcard."""
        request = self._parseService("post.txt").tree.getChild(2)
        postparams = request.getChild(2)
        self.assertEqual(postparams.getChildCount(), 2)
        self.assertEqual(postparams.getChild(0).getText(), 'indoc')
        self.assertEqual(postparams.getChild(1).getText(), '*')
    
    def _parseService(self, service):
        """Parses the service from the given file."""
        s = Service()
        return s.parse("tests/services/" + service)

if __name__ == '__main__':
    unittest.main()
