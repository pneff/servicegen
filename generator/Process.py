import parser.servicegenParser
from tools.Service import DumpTree

class Process:
    """
    Class to process the service to a more readily accessible format.
    """
    def __init__(self, tree):
        self.__service = {}
        self.__config = {}
        self.__requests = []
        self.__variableContext = None
        self.__currentVar = None
        self.__stack = []
        
        self.__getLexerSymbols()
        self.walk(tree)
    
    def getService(self):
        """Returns the service as a hash."""
        return self.__service
    
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
        self.__service = {'docs': {'params': {}},
                          'name': tree.getChild(0).getText()}
        self.__currentVar = self.__service
        self.walktree(tree)
    
    def walk_CONFIG(self, tree):
        # List of variables
        self.__variableContext = self.__config
        self.walktree(tree)
        self.__variableContext = None
    
    def walk_VARIABLE(self, tree):
        name = tree.getChild(1).getText()
        self.__stack.append(self.__currentVar)
        self.__currentVar = {'docs': {'params': {}}}
        self.__currentVar['name'] = tree.getChild(1).getText()
        self.walktree(tree)
        self.__variableContext[name] = self.__currentVar
        self.__currentVar = self.__stack.pop()
    
    def walk_VARTYPE(self, tree):
        self.__currentVar['type'] = tree.getChild(0).getText()
    
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
        self.__currentVar['docs']['params'][tree.getChild(0).getText()] = tree.getChild(1).getText()
    
    def walk_DOC(self, tree):
        self.__currentVar['docs'][tree.getChild(0).getText()] = tree.getChild(1).getText()
    
    def walk_REQUEST(self, tree):
        self.__currentVar = {
            'docs': {'params': {}},
            'vars': {},
            'method': tree.getChild(0).getText(),
            'output': {},
        }
        self.__variableContext = self.__currentVar['vars']
        self.walktree(tree)
        self.__requests.append(self.__currentVar)
        self.__variableContext = None
        self.__currentVar = None
    
    def walk_REQUEST_PATH(self, tree):
        self.__currentVar['path'] = tree.getChild(0).getText()
    
    def walk_STATEMENT_OUTPUT(self, tree):
        self.__stack.append(self.__currentVar)
        self.__currentVar = {'docs': {'params': {}}}
        self.walktree(tree)
        output_type = tree.getChild(0).getText()
        output = self.__currentVar
        self.__currentVar = self.__stack.pop()
        self.__currentVar['output'][output_type] = output
    
    def walk_CACHE(self, tree):
        self.__currentVar['cache'] = {
            'value': tree.getChild(0).getChild(0).getText(),
            'unit':  tree.getChild(0).getText()}
    
    def __getTokenName(self, node):
        """Return the node's type as a string."""
        type = node.getType()
        if type in self.lookup:
            return self.lookup[type]
        else:
            return 'NO_SUCH_TYPE'
