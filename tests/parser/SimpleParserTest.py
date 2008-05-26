import unittest
from parser.Service import Service
from parser.servicegenLexer import servicegenLexer
from tools.Service import DumpTree

class SimpleParserTest(unittest.TestCase):
    def testBasic(self):
        """
        Tests parsing of a very basic service. Just contains the service
        name, nothing else.
        """
        service = self._parseService("basic.txt")
        root = service.tree
        self.assertEqual(root.getChild(0).getText(), 'service')
        self.assertEqual(root.getChild(1).getText(), 'meteo')
    
    def testConfig(self):
        """Tests parsing of a service with a configuration block.
        """
        service = self._parseService("config.txt")
        root = service.tree
        self.assertEqual(root.getChild(0).getText(), 'service')
        self.assertEqual(root.getChild(1).getText(), 'meteo')
        self.assertEqual(root.getChild(3).getText(), 'config')
        self.assertEqual(root.getChild(5).getText(), 'database')
        self.assertEqual(root.getChild(6).getText(), 'db')
        self.assertEqual(root.getChild(8).getText(), 'string')
        self.assertEqual(root.getChild(9).getText(), 'password')
        
        
    def _parseService(self, service):
        """Parses the service from the given file."""
        s = Service()
        return s.parse("tests/services/" + service)

if __name__ == '__main__':
    unittest.main()
