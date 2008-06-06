import web

def validate(value, comparison):
    if comparison.match(value) == None:
        web.ctx.status = '400 Bad Request'
        web.header('Content-Type', 'text/html')
        return web.output('Invalid value "' + value + '"\n')
        

def get_cache(key):
    return None

def set_cache(key, value):
    return True
