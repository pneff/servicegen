import parser.servicegenParser

class Process:
    """
    Class to process the service to a more readily accessible format.
    """
    def __init__(self, tree):
        self.__name = None
        self.__config = {}
        self.__requests = []
        self.__getLexerSymbols()
        self.walk(tree)
    
    def getName(self):
        """Returns the service name as a string."""
        return self.__name
    
    def getConfig(self):
        """Returns the configured variables as a hash."""
        return self.__config
    
    def getRequests(self):
        """Returns all defined requests as an array."""
        return self.__requests
    
    def __getLexerSymbols(self):
        """
        Create a table to be able to look up token IDs and
        return the token symbol.
        """
        tokens = ['SERVICE', 'CONFIG', 'REQUEST']
        self.lookup = {}
        for token in tokens:
            value = getattr(parser.servicegenParser, token)
            self.lookup[value] = token
    
    def walk(self, tree):
        method = 'walk_%s' % self.__getTokenName(tree)
        if hasattr(self, method):
            getattr(self, method)(tree)
        elif tree.getChildCount() > 0:
            for i in range(tree.getChildCount()):
                self.walk(tree.getChild(i))
    
    def walk_SERVICE(self, tree):
        serviceName = tree.getChild(0).getText()
        self.__name = serviceName
    
    def walk_CONFIG(self, tree):
        # List of variables
        for i in range(tree.getChildCount()):
            var = tree.getChild(i)
            vartype = var.getChild(0).getChild(0).getText()
            varname = var.getChild(1).getText()
            varvalue = var.getChild(2)
            if varvalue:
                varvalue = varvalue.getChild(0).getText()
            self.__config[varname] = {'type': vartype, 'value': varvalue}
    
    def walk_REQUEST(self, tree):
        method = tree.getChild(0).getText()
        path = tree.getChild(1).getChild(0).getText()
        tree.deleteChild(0)
        tree.deleteChild(0)
        self.__requests.append(
            {'method'    : method,
             'path'      : path,
             'statements': tree})
    
    def __getTokenName(self, node):
        """Return the node's type as a string."""
        type = node.getType()
        if type in self.lookup:
            return self.lookup[type]
        else:
            return 'NO_SUCH_TYPE'
