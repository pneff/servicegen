import web

def matches(type):
    """Returns true if the current request is of the given type."""
    accept = [
        entry.split(';')[0].split('/')[-1] for entry in
            web.ctx.env.get('HTTP_ACCEPT').split(',')]
    
    if web.ctx.path.endswith('.' + type):
        return True
    if type in accept:
        return True
    return False
