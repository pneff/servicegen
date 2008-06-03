import parser.servicegenParser
from tools.Service import DumpTree

class Process:
    """
    Class to process the service to a more readily accessible format.
    """
    def __init__(self, tree):
        self.__name = None
        self.__config = {}
        self.__requests = []
        self.__getLexerSymbols()
        self.__inConfig = False
        self.__currentVar = {}
        self.__currentRequest = {}
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
        tokens = [method[5:] for method in dir(self) if method[0:5] == 'walk_']
        self.lookup = {}
        for token in tokens:
            value = getattr(parser.servicegenParser, token)
            self.lookup[value] = token
    
    def walktree(self, tree):
        children = tree.getChildCount()
        if children > 0:
            for i in range(children):
                self.walk(tree.getChild(i))
    
    def walk(self, node):
        method = 'walk_%s' % self.__getTokenName(node)
        if hasattr(self, method):
            getattr(self, method)(node)
        else:
            self.walktree(node)
    
    def walk_SERVICE(self, tree):
        serviceName = tree.getChild(0).getText()
        self.__name = serviceName
    
    def walk_CONFIG(self, tree):
        # List of variables
        self.__inConfig = True
        self.walktree(tree)
        self.__inConfig = False
    
    def walk_VARIABLE(self, tree):
        name = tree.getChild(1).getText()
        self.__currentVar = {}
        self.walktree(tree)
        if self.__inConfig:
            self.__config[name] = self.__currentVar
    
    def walk_VARTYPE(self, tree):
        self.__currentVar['type'] = tree.getChild(0).getText()
    
    def walk_VARREF(self, tree):
        self.__currentVar['name'] = tree.getChild(0).getText()
    
    def walk_LITERAL_STRING(self, tree):
        self.__currentVar['value'] = {'type': 'string', 'value': tree.getChild(0).getText()}
    
    def walk_LITERAL_INT(self, tree):
        self.__currentVar['value'] = {'type': 'int', 'value': tree.getChild(0).getText()}
    
    def walk_LITERAL_REGEXP(self, tree):
        self.__currentVar['value'] = {'type': 'regexp', 'value': tree.getChild(0).getText()}
    
    def walk_LITERAL_DURATION(self, tree):
        self.__currentVar['value'] = {'type': 'duration', 'value': tree.getChild(0).getText()}
    
    def walk_LITERAL_XML(self, tree):
        self.__currentVar['value'] = {'type': 'xml', 'value':
            tree.getChild(0).getText() + tree.getChild(1).getText() + tree.getChild(2).getText()}
    
    def walk_DOC_FOR(self, tree):
        self.__currentVar['@desc'] = tree.getChild(1).getText()
    
    def walk_REQUEST(self, tree):
        self.__currentRequest = {}
        self.walktree(tree)
        self.__requests.append(self.__currentRequest)
    
    def __getTokenName(self, node):
        """Return the node's type as a string."""
        type = node.getType()
        if type in self.lookup:
            return self.lookup[type]
        else:
            return 'NO_SUCH_TYPE'
