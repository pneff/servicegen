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
                template = Template(filename=sourcepath)
                for req in self.process.getRequests():
                    print "  - Request: %s" % req['name']
                    out = template.render(service     = self.process.getService(),
                                          servicename = self.process.getService()['name'],
                                          config      = self.process.getConfig(),
                                          requests    = self.process.getRequests(),
                                          req         = req,
                                          getValue    = self.getValue,
                                         )
                    targetpath = targetpath.replace("_request_", req['name'])
                    f = open(targetpath, "w")
                    f.write(out)
                    f.close()
                
            elif is_template:
                print "Processing template %s" % sourcepath
                template = Template(filename=sourcepath)
                out = template.render(service     = self.process.getService(),
                                      servicename = self.process.getService()['name'],
                                      config      = self.process.getConfig(),
                                      requests    = self.process.getRequests(),
                                      getValue    = self.getValue,
                                     )
                f = open(targetpath, "w")
                f.write(out)
                f.close()
            else:
                print "Copying %s => %s" % (sourcepath, targetpath)
                shutil.copyfile(sourcepath, targetpath)
    
    def getValue(self, value):
        type = value['type']
        val = value['value']
        if type == 'string':
            return '"' + val + '"'
        else:
            return value
    
    def __fileSubstitute(self, path):
        return path.replace("_servicename_", self.__serviceName)
