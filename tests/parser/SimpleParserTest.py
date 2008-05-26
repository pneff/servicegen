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
        self.assertEqual(root.getText(), 'service')
        self.assertEqual(root.getChild(0).getType(), parser.servicegenLexer.IDENTIFIER)
        self.assertEqual(root.getChild(0).getText(), 'meteo')
    
    def testConfig(self):
        """Tests parsing of a service with a configuration block.
        """
        service = self._parseService("config.txt")
        root = service.tree
        self.assertEqual(root.getChild(0).getType(), parser.servicegenLexer.SERVICE)
        self.assertEqual(root.getChild(0).getText(), 'service')
        self.assertEqual(root.getChild(0).getChild(0).getText(), 'meteo')
        self.assertEqual(root.getChild(1).getText(), 'config')
        self.assertEqual(root.getChild(3).getText(), 'database')
        self.assertEqual(root.getChild(4).getText(), 'db')
        self.assertEqual(root.getChild(6).getText(), 'string')
        self.assertEqual(root.getChild(7).getText(), 'password')
        
        
    def _parseService(self, service):
        """Parses the service from the given file."""
        s = Service()
        return s.parse("tests/services/" + service)

if __name__ == '__main__':
    unittest.main()
