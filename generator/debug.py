class debug:
    def __init__(self, process):
        self.process = process
    
    def write(self, outputdir):
        name = self.process.getService()['name']
        docs = self.process.getService()['docs']
        config = "\n    - ".join(["%s=%s" % (k, v) for k, v in self.process.getConfig().items()])
        requests = "\n    - ".join([str(item) for item in self.process.getRequests()])
        
        print """
Name:        %(name)s
Docs:        %(docs)s
Config:      
    - %(config)s
Requests:    
    - %(requests)s""" % locals()
