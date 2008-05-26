#!/usr/bin/python
import unittest
from tests.parser.SimpleParserTest import SimpleParserTest

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(SimpleParserTest)
    unittest.TextTestRunner(verbosity=2).run(suite)

