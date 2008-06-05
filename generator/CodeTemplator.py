import os, os.path, shutil
from mako.template import Template

class CodeTemplator:
    """
    Walks a directory (set with the template option)
    and generates code files from all templates. All
    non-template files and directories are copied over
    to the target directory.
    """
    __options = {}
    __outdir = '/tmp/'
    
    def __init__(self, process):
        self.process = process
    
    def setOption(self, key, value):
        self.__options[key] = value
    
    def write(self, outputdir):
        template = self.__options['template']
        self.__outdir = outputdir
        self.__serviceName = self.process.getService()['name']
        
        for root, dirs, files in os.walk(template):
            path = root[len(template):]
            self.__processFiles(path, files)
    
    def __processFiles(self, path, files):
        for file in files:
            is_template = (file.find('.tmpl') != -1)
            basename = self.__fileSubstitute(file.replace('.tmpl', ''))
            targetdir = self.__fileSubstitute(self.__outdir + path)
            targetpath = targetdir + '/' + basename
            sourcepath = self.__options['template'] + path + '/' + file
            if not os.path.exists(targetdir):
                os.makedirs(targetdir)
            
            if is_template and file.find("_request_") > -1:
                # Once for each request
                print "Processing template %s" % sourcepath
                for req in self.process.getRequests():
                    print "  - Request: %s" % req['name']
                    self.render(sourcepath, targetpath.replace("_request_", req['name']),
                                req=req)
            elif is_template:
                print "Processing template %s" % sourcepath
                self.render(sourcepath, targetpath)
            else:
                print "Copying %s => %s" % (sourcepath, targetpath)
                shutil.copyfile(sourcepath, targetpath)
    
    def render(self, template, targetpath, **data):
        template = Template(filename=template)
        data_def = {'service'    : self.process.getService(),
                    'servicename': self.process.getService()['name'],
                    'config'     : self.process.getConfig(),
                    'requests'   : self.process.getRequests(),
                    'getValue'   : self.getValue,
                   }
        data_def.update(data)
        out = template.render(**data_def)
        f = open(targetpath, "w")
        f.write(out)
        f.close()
    
    def getValue(self, value):
        """Returns the value in the target language."""
        type = value['type']
        val = value['value']
        if type == 'string' or type == 'LITERAL_STRING':
            return '"' + val + '"'
        elif type == 'VARREF':
            return val
        elif type == 'LITERAL_REGEXP':
            return 're.compile(\'^' + val[1:-1] + '$\')'
        else:
            print "Unhandled type in getValue: %s" % type
            return val
    
    def __fileSubstitute(self, path):
        return path.replace("_servicename_", self.__serviceName)
