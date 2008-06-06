import web

class TerminateRequest(Exception):
    """Exception thrown when the request should be terminated."""
    pass

def validate(value, comparison):
    matches = True
    try:
        matches = (comparison.match(value) != None)
    except AttributeError:
        matches = (str(value) == str(comparison))
    if not matches:
        web.ctx.status = '400 Bad Request'
        web.header('Content-Type', 'text/html')
        web.output('Invalid value "' + value + '"\n')
        raise TerminateRequest, 'Invalid value "' + value + '"'

def get_cache(key):
    return None

def set_cache(key, value):
    return True
