import copy, re

class HtmlDoc:
    """Generates HTML documentation."""
    START = """<html>
    <head><title>Service {SERVICE_NAME}</title></head>
    <body>
        <h1>Service {SERVICE_NAME}</h1>"""
    
    END = """</body></html>"""
    
    def __init__(self, process):
        self.process = process
    
    def write(self, outputdir):
        f = open(outputdir + "/index.html", "w")
        f.write(self.__replace(self.START))
        
        self.__writeService(f)
        self.__writeConfig(f)
        self.__writeRequests(f)
        
        f.write(self.__replace(self.END))
        f.close()
    
    def __replace(self, str):
        name = self.process.getService()['name']
        return str.replace('{SERVICE_NAME}', name)
    
    def __writeService(self, f):
        docs = self.process.getService()['docs']
        self.__writeDocTable(f, docs)
        f.write("<hr />")
    
    def __writeConfig(self, f):
        f.write("<h2>Configuration</h2>")
        f.write("<p>These variables can be changed using the external config file.</p>")
        
        for key, value in self.process.getConfig().items():
            f.write("<h3><em class=\"type\">" + value['type'] + "</em> " + key + "</h3>")
            self.__writeDocTable(f, value['docs'])
        f.write("<hr />")
    
    def __writeRequests(self, f):
        f.write("<h2>Requests</h2>")
        self.__writeRequestsTable(f)
        self.__writeRequestsDetails(f)
    
    def __writeRequestsTable(self, f):
        f.write("<h3>Summary</h3>")
        f.write('<table class="requests">')
        requests = self.process.getRequests()
        for req in requests:
            doc = ''
            if req['docs'].has_key('doc'):
                doc = req['docs']['doc']
            f.write('<tr><td>%s</td><td><a href="%s">%s</a><br />%s</td></tr>' %
                (req['method'], '#req' + self.__makeId(req['method'] + '_' + req['path']),
                 req['path'], doc))
            print req
        f.write('</table><hr />')
    
    def __writeRequestsDetails(self, f):
        requests = self.process.getRequests()
        for req in requests:
            f.write('<h3 id="%s"><em class="method">%s</em> %s</h3>' % (
                self.__makeId(req['method'] + '_' + req['path']),
                req['method'], req['path']))
            self.__writeDocTable(f, req['docs'])
    
    def __writeDocTable(self, f, docs):
        docs = copy.deepcopy(docs)
        if docs.has_key('doc'):
            f.write("<p>" + docs['doc'] + "</p>\n")
            del docs['doc']
        if docs.has_key('params') and len(docs['params']) > 0:
            f.write('<h4>Params</h4>')
            f.write("<dl>")
            for key, value in docs['params'].iteritems():
                f.write("<dt>" + key + "</dt>")
                f.write("<dd>" + value + "</dd>")
            f.write("</dl>")
        del docs['params']
        if len(docs) > 0:
            f.write("<dl>")
            for key, value in docs.iteritems():
                f.write("<dt>" + key + "</dt>")
                f.write("<dd>" + value + "</dd>")
            f.write("</dl>")
    
    def __makeId(self, str):
        return re.sub('[^a-zA-Z0-9_]', '_', str)
