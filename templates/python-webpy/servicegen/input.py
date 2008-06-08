import web, cgi
from cStringIO import StringIO
from servicegen.function import TerminateRequest

def get(key):
    if key[-1] == '*':
        return web.data()
    else:
        # Get POST data. Can't use web.input() as it
        # only works for POST method, not PUT
        e = web.ctx.env.copy()
        if e['REQUEST_METHOD'] in ['GET', 'POST']:
            input = cgi.FieldStorage(environ=e, keep_blank_values=1)
        else:
            input = cgi.FieldStorage(fp = StringIO(web.data()), environ=e,
                                     keep_blank_values=1)
        
        if key in input:
            return input[key].value
        else:
            web.ctx.status = '400 Bad Request'
            web.header('Content-Type', 'text/html')
            web.output('Missing value "' + key + '"\n')
            raise TerminateRequest, 'Missing value "' + key + '"'
