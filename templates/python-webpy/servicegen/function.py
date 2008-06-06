import web

def validate(value, comparison):
    matches = True
    try:
        matches = (comparison.match(value) != None)
    except AttributeError:
        matches = (str(value) == str(comparison))
    if not matches:
        web.ctx.status = '400 Bad Request'
        web.header('Content-Type', 'text/html')
        return web.output('Invalid value "' + value + '"\n')
        

def get_cache(key):
    return None

def set_cache(key, value):
    return True
