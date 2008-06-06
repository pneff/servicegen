import sys, web, csv
from xml.sax.saxutils import escape

def best_of(types):
    """
    Returns the best output type of `types' to fullfil the current request.
    """
    
    # Path takes priority
    for type in types:
        if web.ctx.path.endswith('.' + type):
            return type
    
    # Try accept header
    accept = [
        entry.split(';')[0].split('/')[-1] for entry in
            web.ctx.env.get('HTTP_ACCEPT').split(',')]
    for type in accept:
        if type in types:
            return type
    
    # Return first entry (to be changed)
    return types[0]

def get_outputter(out_type):
    return globals()['Outputter' + out_type.upper()]()


class Outputter:
    def header(self):
        pass
    
    def write(self, value_type, value):
        pass
    
    def write_records(self, value, varname):
        pass
    
    def write_array(self, value, varname):
        pass
    
    def write_hash(self, value, varname):
        pass


class OutputterXML(Outputter):
    def header(self):
        web.header('Content-Type', 'text/xml; charset=utf-8', unique=True)
    
    def write(self, value_type, value):
        if value_type == 'LITERAL_XML' or value_type == 'dom':
            return web.output(value)
        else:
            return web.output(escape(str(value)))
    
    def write_records(self, value, varname):
        for item in value:
            web.output('<' + varname + '>')
            self.write_hash(item, varname)
            web.output('</' + varname + '>')
    
    def write_array(self, value, varname):
        for item in value:
            web.output('<' + varname + '>' + 
                       escape(str(item)) +
                       '</' + varname + '>')
    
    def write_hash(self, value, varname):
        for key, val in value.iteritems():
            web.output('<' + key + '>' + 
                       escape(str(val)) +
                       '</' + key + '>')


class OutputterCSV(Outputter):
    def header(self):
        web.header('Content-Type', 'text/csv; charset=utf-8', unique=True)
    
    def write(self, value_type, value):
        web.output(value)
        web.output("\t")
    
    def write_records(self, value, varname):
        # Header
        if len(value) > 0:
            for key in value[0]:
                web.output(key)
                web.output("\t")
            web.output("\n")
        # Each record
        for item in value:
            self.write_hash(item, varname)
            web.output("\n")
    
    def write_array(self, value, varname):
        for item in value:
           web.output(item)
           web.output("\t")
    
    def write_hash(self, value, varname):
        for key, val in value.iteritems():
            web.output(val)
            web.output("\t")
